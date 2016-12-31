# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#range_filter' do
    it 'returns a javascript range filter' do
      filter = context.range_filter(
        label: 'Year', attribute: 'data-year', min: '1959', max: '2014'
      )
      expect(filter).to eq(
        '<div class="filter-control">' \
        '<label for="year" class="filter-label">Year</label>' \
        '<div class="filter-range" data-filter-attribute="data-year" ' \
        'data-filter-type="range" data-filter-min-value="1959" ' \
        'data-filter-max-value="2014"><div class="noUiSlider noUi-target">' \
        '<div class="noUi-base noUi-background noUi-horizontal">' \
        '<div class="noUi-origin noUi-origin-lower" style="left: 0%;">' \
        '<div class="noUi-handle noUi-handle-lower"></div></div>' \
        '<div class="noUi-origin noUi-origin-upper" style="left: 100%;">' \
        '<div class="noUi-handle noUi-handle-upper"></div></div></div></div>' \
        '<input type="number" value="1959" min="1959" max="2014" step="1" ' \
        'class="filter-numeric min" /><input type="number" value="2014" min="1959" ' \
        'max="2014" step="1" class="filter-numeric max" /></div></div>'
      )
    end
  end
end
