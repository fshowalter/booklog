# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#select_filter' do
    it 'returns a javascript select filter' do
      filter = context.select_filter(
        label: 'Venue',
        attribute: 'venue',
        options: [['venue 1', 0], ['venue 2', 1]]
      )

      expect(filter).to eq(
        '<div class="filter-control">' \
        '<label for="venue" class="filter-label">Venue</label>' \
        '<select name="venue" class="filter-select" ' \
        'data-filter-attribute="venue" data-filter-type="select">' \
        "<option value=\"\">All</option>\n" \
        "<option value=\"0\">venue 1</option>\n" \
        "<option value=\"1\">venue 2</option>\n</select></div>"
      )
    end
  end
end
