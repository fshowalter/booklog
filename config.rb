require 'booklog/booklog'
require 'active_support/core_ext/array/conversions'
require 'time'

# Reload the browser automatically whenever files change
configure :development do
  activate :livereload
end

helpers Booklog::Helpers

# Methods defined in the helpers block are available in templates
helpers do
  def markdown(source)
    Tilt['markdown'].new(smartypants: true) { source }.render
  end

  def published_date(date)
    date.iso8601
  end

  def authors_to_links(authors)
    authors.reduce([]) do |memo, author_name|
      author = Booklog.authors[author_name]
      memo << link_to(author_name, "/authors/#{author.slug}/")
    end.to_sentence
  end
end

set :css_dir, 'stylesheets'
set :js_dir, 'javascripts'
set :images_dir, 'images'

set :markdown_engine, :redcarpet

set :haml, remove_whitespace: true

page 'feed.xml', mime_type: 'text/xml'

activate :directory_indexes

activate :autoprefixer do |config|
  config.browsers = ['last 2 versions', 'Explorer >= 9', 'Firefox ESR']
end

activate :pagination do
  pageable_set :reviews do
    Booklog.reviews.keys.sort.reverse
  end

  pageable_set :posts do
    Booklog.posts.keys.sort.reverse
  end

  pageable_set :authors do
    Booklog.authors.keys.sort
  end
end

activate :deploy do |deploy|
  deploy.method = :git
  deploy.build_before = true
end

activate :sitemap, hostname: 'http://booklog.frankshowalter.com'

# Build-specific configuration
configure :build do
  activate :minify_css
  activate :minify_javascript

  # Enable cache buster
  activate :asset_hash

  # Use relative URLs
  activate :relative_assets

  activate :gzip
end

ready do
  Booklog.reviews.each do |_id, review|
    proxy("reviews/#{review.slug}.html", 'review.html',
          locals: { review: review }, ignore: true)
  end

  # Booklog::App.features.each do |_id, feature|
  #   raise feature.inspect
  #   proxy("features/#{feature.slug}.html", 'feature.html',
  #         locals: { feature: feature, title: "#{feature.title}" }, ignore: true)
  # end

  # Booklog::App.authors.each do |id, author|
  #   proxy("authors/#{author.slug}.html", 'author.html',
  #         locals: { author: author, title: "#{author.name}" }, ignore: true)
  # end
end
