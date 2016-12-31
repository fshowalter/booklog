# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def filter_control_label(label:)
      label_tag(label, caption: label, class: 'filter-label', for: filter_control_attribute(label))
    end
  end
end
