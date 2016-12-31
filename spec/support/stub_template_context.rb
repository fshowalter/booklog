# frozen_string_literal: true
require 'padrino-helpers'

module Movielog
  #
  # Responsible for providing helper methods to test template helpers.
  #
  module TemplateContextHelper
    def stub_template_context
      StubTemplateContext.new
    end
  end

  #
  # Responsible for initializing a testable instance of the template helpers.
  #
  class StubTemplateContext
    include ::Padrino::Helpers::OutputHelpers
    include ::Padrino::Helpers::TagHelpers
    include ::Padrino::Helpers::AssetTagHelpers
    include ::Padrino::Helpers::FormHelpers
    include ::Padrino::Helpers::FormatHelpers
    include ::Padrino::Helpers::RenderHelpers
    include ::Padrino::Helpers::NumberHelpers

    # require 'middleman-more/core_extensions/default_helpers'
    # Middleman::CoreExtensions::DefaultHelpers.defined_helpers.each do |helper|
    #   include helper
    # end

    Dir[File.expand_path('../../../movielog/helpers/*.rb', __FILE__)].each do |file|
      require file
    end

    def image_tag(file, _options)
      file
    end

    def image_path(file)
      file
    end

    def development?
      @development = true if @development.nil?
      @development
    end

    attr_writer :development

    include Movielog::Helpers
  end
end

RSpec.configure do |config|
  config.include(Movielog::TemplateContextHelper)
end
