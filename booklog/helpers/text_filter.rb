# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def text_filter(label:, placeholder:, attribute:)
      options = {}
      options['placeholder'] = placeholder
      options['class'] = 'filter-text_box'
      options['data'] = {}
      options['data']['filter-attribute'] = attribute
      options['data']['filter-type'] = 'text'

      field_tag = text_field_tag(label.downcase, options)

      filter_control(control: content_tag(
        :div, field_tag, class: 'filter-text_box_wrap'
      ), label: label)
    end
  end
end
