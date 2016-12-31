# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def data_for_person(person:, credits_method:)
      {
        data: {
          sort_name: person.full_name,
          name: "#{person.first_name} #{person.last_name}",
          review_count: person.send(credits_method).length.to_s.rjust(3, '0')
        }
      }
    end
  end
end
