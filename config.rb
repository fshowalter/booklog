require 'booklog'
require 'active_support/core_ext/array/conversions'
require 'time'

###
# Page options, layouts, aliases and proxies
###

# Per-page layout changes:
#
# With no layout
# page "/path/to/file.html", :layout => false
#
# With alternative layout
# page "/path/to/file.html", :layout => :otherlayout
#
# A path which all have the same layout
# with_layout :admin do
#   page "/admin/*"
# end

# Proxy pages (http://middlemanapp.com/basics/dynamic-pages/)
# proxy "/this-page-has-no-template.html", "/template-file.html", :locals => {
#  :which_fake_page => "Rendering a fake page with a local variable" }

# Reload the browser automatically whenever files change
configure :development do
  activate :livereload
end

###
# Helpers
###

# Automatic image dimensions on image_tag helper
# activate :automatic_image_sizes

# Methods defined in the helpers block are available in templates
helpers do
  def site
    OpenStruct.new(YAML.load_file('config.yml'))
  end

  def markdown(source)
    Tilt['markdown'].new { source }.render
  end

  def published_date(review)
    review.date.iso8601
  end

  def description_for_review(review, aka_titles)
    description = "A review of #{review.display_title}"

    return "#{description}." unless aka_titles.any?

    "#{description}, also known as #{aka_titles.map(&:aka_title).to_sentence}."
  end

  ###
  # Ratings
  ###

  def grade_to_number(grade)
    return if grade.blank?

    case grade
    when 'A+'
      15
    when 'A'
      14
    when 'A-'
      13
    when 'B+'
      12
    when 'B'
      11
    when 'B-'
      10
    when 'C+'
      9
    when 'C'
      8
    when 'C-'
      7
    when 'D+'
      6
    when 'D'
      5
    when 'D-'
      4
    when 'F'
      1
    end
  end

  def grade_to_text(grade)
    return if grade.blank?

    case grade
    when 'A+'
      '★★★★★'
    when 'A'
      '★★★★½'
    when 'A-'
      '★★★★☆'
    when 'B+'
      '★★★½☆'
    when 'B'
      '★★★☆☆'
    when 'B-'
      '★★★☆☆'
    when 'C+'
      '★★½☆☆'
    when 'C'
      '★★½☆☆'
    when 'C-'
      '★★½☆☆'
    when 'D+'
      '★★☆☆☆'
    when 'D'
      '★½☆☆☆'
    when 'D-'
      '★½☆☆☆'
    when 'F'
      '★☆☆☆☆'
    end
  end

  # rubocop:disable LineLength
  def grade_to_stars(grade)
    return if grade.blank?

    stars =
      case grade
      when 'A+'
        [star, star(1), star(2), star(3), star(4)].join
      when 'A'
        [star, star(1), star(2), star(3), half_star(4)].join
      when 'A-'
        [star, star(1), star(2), star(3), half_star(4)].join
      when 'B+'
        [star, star(1), star(2), star(3), empty_star(4)].join
      when 'B'
        [star, star(1), star(2), half_star(3), empty_star(4)].join
      when 'B-'
        [star, star(1), star(2), half_star(3), empty_star(4)].join
      when 'C+'
        [star, star(1), star(2), empty_star(3), empty_star(4)].join
      when 'C'
        [star, star(1), half_star(2), empty_star(3), empty_star(4)].join
      when 'C-'
        [star, star(1), half_star(2), empty_star(3), empty_star(4)].join
      when 'D+'
        [star, star(1), empty_star(2), empty_star(3), empty_star(4)].join
      when 'D'
        [star, half_star(1), empty_star(2), empty_star(3), empty_star(4)].join
      when 'D-'
        [star, half_star(1), empty_star(2), empty_star(3), empty_star(4)].join
      when 'F'
        [star, empty_star(1), empty_star(2), empty_star(3), empty_star(4)].join
      end

    <<-SVG
      <svg class="rating" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 2560 512">
        #{stars}
      </svg>
    SVG
  end

  def star(index = 0)
    <<-SVG
      <polygon transform="translate(#{512 * index})" class="star" points="256,389.375 97.781,499.477 153.601,314.977 0,198.523 192.71,194.59 256,12.523 319.297,194.59 512,198.523 358.399,314.977 414.226,499.477 "/>
    SVG
  end

  def half_star(index = 0)
    <<-SVG
      <path transform="translate(#{512 * index})" class="empty-star" d="M 512,198.523 319.289,194.594 256,12.525 192.707,194.594 0,198.526 153.599,314.975 97.784,499.475 255.996,389.381 414.225,499.475 358.394,314.975 512,198.526 z M 359.201,423.656 256,351.744 V 106.115 l 41.284,118.766 125.701,2.559 -100.199,75.969 36.415,120.247 z" />
      <path transform="translate(#{512 * index})" class="star" d="M 256,16.638245 193.39062,194.82574 0.67187503,198.76324 154.26562,315.20075 l -55.812495,184.5 156.874995,-109.15625 0,-373.906255 z" />
    SVG
  end

  def empty_star(index = 0)
    <<-SVG
      <path transform="translate(#{512 * index})" class="empty-star" d="M512,198.52l-192.709-3.924L255.995,12.524l-63.288,182.071L0,198.52l153.599,116.463L97.781,499.476l158.214-110.103 l158.229,110.103l-55.831-184.493L512,198.52z M359.202,423.764L255.994,351.94l-103.207,71.823l36.414-120.35L89.003,227.448 l125.708-2.566l41.292-118.773l41.283,118.773l125.699,2.566l-100.2,75.967L359.202,423.764z"/>
    SVG
  end
  # rubocop:enable LineLength

  ###
  # Filters
  ###

  def filter_control(control, label = nil)
    label = filter_control_label(label) if label

    content_tag(:div, class: 'filter-control') do
      [
        label,
        control
      ].join.html_safe
    end
  end

  def sort_filter(label, attribute, target, options)
    html_options = {}
    html_options['class'] = 'filter-select'
    data = {}
    data['sorter'] = attribute
    data['target'] = target
    html_options['data'] = data
    html_options[:options] = options
    field_tag = select_tag(filter_control_attribute(attribute), html_options)
    filter_control(content_tag(:div, field_tag, class: 'sort-wrap'), label)
  end

  def oldest_year(collection, date_method)
    collection.map(&date_method).sort.first.year
  end

  def newest_year(collection, date_method)
    collection.map(&date_method).sort.reverse.first.year
  end

  def filter_control_label(label)
    label_tag(label, class: 'filter-label', for: filter_control_attribute(label))
  end

  def filter_control_attribute(text)
    text.downcase.gsub(' ', '-')
  end

  def text_filter(placeholder, attribute)
    options = {}
    options['placeholder'] = placeholder
    options['class'] = 'filter-text-box'
    options['data'] = {}
    options['data']['filter-attribute'] = attribute
    options['data']['filter-type'] = 'text'

    field_tag = text_field_tag(attribute, options)

    filter_control(content_tag(:div, field_tag, class: 'search-wrap clearable-wrap'))
  end

  def range_filter(label, attribute, min, max)
    data = {}
    data['filter-attribute'] = attribute
    data['filter-type'] = 'range'
    data['filter-min-value'] = min
    data['filter-max-value'] = max
    options = {}
    options['class'] = 'filter-range'
    options['data'] = data

    control = content_tag(:div, options) do
      [
        content_tag(:div, class: 'noUiSlider noUi-target') do
          content_tag(:div, class: 'noUi-base noUi-background noUi-horizontal') do
            [
              content_tag(
                :div,
                content_tag(:div, nil, class: 'noUi-handle noUi-handle-lower'),
                class: 'noUi-origin noUi-origin-lower', style: 'left: 0%;'),
              content_tag(
                :div,
                content_tag(:div, nil, class: 'noUi-handle noUi-handle-upper'),
                class: 'noUi-origin noUi-origin-upper', style: 'left: 100%;')
            ].join.html_safe
          end
        end,
        content_tag(:div, min, class: 'filter-range__min'),
        content_tag(:div, max, class: 'filter-range__max')
      ].join.html_safe
    end

    filter_control(control, label)
  end
end

set :css_dir, 'stylesheets'

set :js_dir, 'javascripts'

set :images_dir, 'images'

set :markdown_engine, :redcarpet

page 'feed.xml', mime_type: 'text/xml'

activate :directory_indexes

activate :autoprefixer

activate :pagination do
  pageable_set :reviews do
    Booklog::App.reviews.keys.sort.reverse
  end

  pageable_set :posts do
    Booklog::App.posts.keys.sort.reverse
  end
end

activate :deploy do |deploy|
  deploy.method = :git
  deploy.build_before = true
end

activate :sitemap, hostname: 'http://booklog.frankshowalter.com'

# Build-specific configuration
configure :build do
  # For example, change the Compass output style for deployment
  # activate :minify_css

  # Minify Javascript on build
  # activate :minify_javascript

  # Enable cache buster
  # activate :asset_hash

  # Use relative URLs
  # activate :relative_assets

  # Or use a different image path
  # set :http_prefix, "/Content/images/"
end

ready do
  Booklog::App.reviews.each do |_id, review|
    proxy("reviews/#{review.slug}.html", 'review.html',
          locals: { review: review, title: "#{review.display_title} Book Review" }, ignore: true)
  end

  Booklog::App.features.each do |_id, feature|
    proxy("features/#{feature.slug}.html", 'feature.html',
          locals: { feature: feature, title: "#{feature.title}" }, ignore: true)
  end
end
