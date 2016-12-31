# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def sort_filter(label:, attribute:, target:, options:)
      html_options = {}
      html_options['class'] = 'filter-select'
      data = {}
      data['sorter'] = attribute
      data['target'] = target
      html_options['data'] = data
      html_options[:options] = options
      field_tag = select_tag(filter_control_attribute(label.downcase), html_options)
      filter_control(control: field_tag, label: label)
    end
  end
end
