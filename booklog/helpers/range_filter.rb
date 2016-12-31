# frozen_string_literal: true
module Booklog
  #
  # Responsible for providing template helper methods.
  #
  module Helpers
    def range_filter(label:, attribute:, min:, max:)
      control = BuildRangeFilter.call(context: self, attribute: attribute, min: min, max: max)

      filter_control(control: control, label: label)
    end

    #
    # Responsible for building range filters.
    #
    class BuildRangeFilter
      class << self
        def call(context:, attribute:, min:, max:)
          options = range_filter_options(attribute: attribute, min: min, max: max)
          context.content_tag(:div, options) do
            [
              build_slider(context: context),
              context.input_tag(:number, value: min, min: min, max: max, step: 1, class: 'filter-numeric min'),
              context.input_tag(:number, value: max, min: min, max: max, step: 1, class: 'filter-numeric max')
            ].join.html_safe
          end
        end

        private

        def build_slider(context:)
          context.content_tag(:div, class: 'noUiSlider noUi-target') do
            context.content_tag(:div, class: 'noUi-base noUi-background noUi-horizontal') do
              [
                build_slider_handle(context: context, position: 'lower', left: '0%'),
                build_slider_handle(context: context, position: 'upper', left: '100%')
              ].join.html_safe
            end
          end
        end

        def build_slider_handle(context:, position:, left:)
          context.content_tag(
            :div,
            context.content_tag(:div, nil, class: "noUi-handle noUi-handle-#{position}"),
            class: "noUi-origin noUi-origin-#{position}", style: "left: #{left};"
          )
        end

        def range_filter_options(attribute:, min:, max:)
          {
            'class' => 'filter-range',
            'data' => {
              'filter-attribute' => attribute,
              'filter-type' => 'range',
              'filter-min-value' => min,
              'filter-max-value' => max
            }
          }
        end
      end
    end
  end
end
