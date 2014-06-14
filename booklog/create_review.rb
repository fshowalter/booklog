require 'active_support/core_ext/hash/slice'

module Booklog
  #
  # Responsible for creating new viewing instances.
  #
  class CreateReview
    class << self
      def call(reviews_path, review)
        file_name = new_review_file_name(reviews_path, review[:slug])

        data = review.slice(
          :sequence, 
          :title, 
          :slug, 
          :authors, 
          :page_count, 
          :year_published, 
          :date_started, 
          :date_finished)

        content = "#{data.to_yaml}---\n"
        File.open(file_name, 'w') { |file| file.write(content) }

        file_name
      end

      private

      def new_review_file_name(reviews_path, slug)
        File.join(reviews_path, slug + '.md')
      end
    end
  end
end
