# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def select_filter(label:, attribute:, options:)
      html_options = {}
      html_options['class'] = 'filter-select'
      data = {}
      data['filter-attribute'] = attribute
      data['filter-type'] = 'select'
      html_options['data'] = data
      html_options[:options] = options
      html_options[:include_blank] = 'All'
      field_tag = select_tag(filter_control_attribute(label.downcase), html_options)
      filter_control(control: field_tag, label: label)
    end
  end
end
