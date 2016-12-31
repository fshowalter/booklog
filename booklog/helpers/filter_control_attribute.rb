# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def filter_control_attribute(text)
      text.downcase.tr(' ', '-')
    end
  end
end
