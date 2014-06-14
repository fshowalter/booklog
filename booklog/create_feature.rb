require 'active_support/core_ext/hash/slice'

module Booklog
  #
  # Responsible for creating new feature instances.
  #
  class CreateFeature
    class << self
      def call(features_path, feature)
        file_name = new_feature_file_name(features_path, feature[:slug])

        content = "#{feature.slice(:sequence, :title, :slug, :date).to_yaml}---\n"
        File.open(file_name, 'w') { |file| file.write(content) }

        file_name
      end

      private

      def new_feature_file_name(features_path, slug)
        File.join(features_path, slug + '.md')
      end
    end
  end
end
