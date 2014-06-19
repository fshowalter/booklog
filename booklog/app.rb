require 'active_support/core_ext/array/conversions'

module Booklog
  #
  # Responsible for serving as an entry-point for the Booklog API.
  #
  class App
    class << self
      def reviews
        ParseReviews.call(reviews_path) || {}
      end

      def features
        ParseFeatures.call(features_path) || {}
      end

      def posts
        features.merge(reviews)
      end

      def authors
        reviews.reduce({}) do |memo, (_sequence, review)|
          review.authors.each do |author|
            memo[author] ||= Author.new(name: author)
            memo[author].slug ||= slugize(author)
            memo[author].titles ||= {}
            memo[author].titles[review.title] = review
          end
          memo
        end
      end

      def create_review(review_hash)
        review_hash[:date] = Date.today
        review_hash[:sequence] = posts.length + 1
        review_hash[:slug] = slugize(
          "#{review_hash[:title]} by #{review_hash[:authors].to_sentence}")
        CreateReview.call(reviews_path, review_hash)
      end

      def create_feature(feature_hash)
        feature_hash[:date] = Date.today
        feature_hash[:sequence] = posts.length + 1
        feature_hash[:slug] = slugize(feature_hash[:title])
        CreateFeature.call(features_path, feature_hash)
      end

      private

      def slugize(words, slug = '-')
        slugged = words.encode('UTF-8', invalid: :replace, undef: :replace, replace: '?')
        slugged.gsub!(/&/, 'and')
        slugged.gsub!(/:/, '')
        slugged.gsub!(/[^\w_\-#{Regexp.escape(slug)}]+/i, slug)
        slugged.gsub!(/#{slug}{2,}/i, slug)
        slugged.gsub!(/^#{slug}|#{slug}$/i, '')
        url_encode(slugged.downcase)
      end

      def url_encode(word)
        URI.escape(word, /[^\w_+-]/i)
      end

      def reviews_path
        File.expand_path('../../reviews/', __FILE__)
      end

      def features_path
        File.expand_path('../../features/', __FILE__)
      end
    end
  end
end
