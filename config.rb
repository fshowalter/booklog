# frozen_string_literal: true
require 'booklog/booklog'
require 'active_support/core_ext/array/conversions'
require 'active_support/core_ext/integer/inflections'
require 'time'

# Reload the browser automatically whenever files change
configure :development do
  activate :livereload, ignore: [%r{/coverage/}, /\.haml_lint\./]
end

helpers Booklog::Helpers

# Methods defined in the helpers block are available in templates
helpers do
  def href_for_review(review)
    "/reviews/#{review.book_id}/"
  end

  def markdown(source)
    return source if source.blank?

    Tilt['markdown'].new(footnotes: true) { source }.render
  end

  def author_link(author:, options: {})
    link_to(author.name, "/authors/#{author.slug}/", options)
  end

  def inline_css(_file)
    filename = File.expand_path("../#{yield_content(:inline_css)}", __FILE__)
    style = Tilt['scss'].new { File.open(filename, 'rb', &:read) }.render

    Middleman::Extensions::MinifyCss::SassCompressor.compress(style)
  end

  def first_paragraph(source)
    return source if source.blank?

    source = source.split("\n\n", 2)[0]

    Tilt['markdown'].new { source }.render.gsub(/\[\^\d\]/, '')
  end
end

set :css_dir, 'stylesheets'
set :js_dir, 'javascripts'
set :images_dir, 'images'

set :markdown_engine, :redcarpet
set :markdown, footnotes: true

set :haml, remove_whitespace: true

page 'feed.xml', mime_type: 'text/xml'

activate :directory_indexes

page '/googlee90f4c89e6c3d418.html', directory_index: false

ignore 'templates/*'
ignore 'redirect.html.haml'

activate :autoprefixer do |config|
  config.inline = true
  config.browsers = ['last 2 versions', 'Firefox ESR']
end

activate :pagination do
  pageable_set :reviews do
    Booklog.reviews_by_sequence
  end
end

activate :deploy do |deploy|
  deploy.method = :git
  deploy.build_before = true
  deploy.clean = true
end

activate :sitemap, hostname: 'https://booklog.frankshowalter.com'

# Build-specific configuration
configure :build do
  activate :minify_css
  activate :minify_javascript
  activate :minify_html, remove_input_attributes: false, remove_http_protocol: false

  set :js_compressor, Uglifier.new(output: { comments: :jsdoc })

  # Enable cache buster
  activate :asset_hash

  # Use relative URLs
  # activate :relative_assets

  activate :gzip
end

ready do
  proxy('index.html', 'templates/home/home.html', ignore: true)
  proxy('404.html', 'templates/404/404.html', directory_index: false, ignore: true)
  proxy('readings/index.html', 'templates/readings/readings.html', ignore: true)
  proxy('reviews/index.html', 'templates/reviews/reviews.html', ignore: true)
  proxy('how-i-grade/index.html', 'templates/how_i_grade/how_i_grade.html', ignore: true)
  proxy('on-abandoning-books/index.html', 'templates/on_abandoning_books/on_abandoning_books.html', ignore: true)
  proxy('authors/index.html', 'templates/authors/authors.html', ignore: true)

  Booklog.reviews.values.each do |review|
    book = Booklog.books[review.book_id]
    proxy("reviews/#{review.book_id}/index.html", 'templates/review/review.html',
          locals: { review: review, title: "#{book.title_with_author} Book Review" }, ignore: true)
  end

  Booklog.authors.values.each do |author|
    proxy("authors/#{author.slug}/index.html", 'templates/reviews_for_author/reviews_for_author.html',
          locals: { author: author }, ignore: true)
  end
end

require 'sass'
require 'cgi'

Sass.load_paths << File.expand_path(File.dirname(__FILE__))

#
# Opened to add the encode_svg helper function.
#
module Sass::Script::Functions # rubocop:disable Style/ClassAndModuleChildren
  def encode_svg(svg)
    encoded_svg = CGI.escape(svg.value).gsub('+', '%20')
    data_url = "url('data:image/svg+xml;charset=utf-8," + encoded_svg + "')"
    Sass::Script::String.new(data_url)
  end
end

#
# Opened to fix build deleting the .git directory.
#
class Middleman::Cli::BuildAction < ::Thor::Actions::EmptyDirectory # rubocop:disable Style/ClassAndModuleChildren
  # Remove files which were not built in this cycle
  # @return [void]
  def clean!
    @to_clean.each do |f|
      base.remove_file(f, force: true) unless f =~ /\.git/
    end

    ::Middleman::Util.glob_directory(@build_dir.join('**', '*'))
                     .select { |d| File.directory?(d) }
                     .each do |d|
      base.remove_file d, force: true if directory_empty? d
    end
  end
end
