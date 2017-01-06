# frozen_string_literal: true
module Booklog
  class Author
    attr_reader :id, :name, :name_with_annotation, :sortable_name, :url

    def initialize(id:, name:, name_with_annotation:, sortable_name:, url:)
      @id = id
      @name = name
      @name_with_annotation = name_with_annotation
      @sortable_name = sortable_name
      @url = url
    end
  end
end
