# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#sort_filter' do
    it 'returns a javascript range filter' do
      filter = context.sort_filter(
        label: 'Order By',
        attribute: 'viewing-date-desc',
        target: '#viewings',
        options: [
          %w(Title title-asc),
          %w(Newest release-date-desc),
          %w(Oldest release-date-asc),
          ['Newest Viewing', 'viewing-date-desc'],
          ['Oldest Viewing', 'viewing-date-asc']
        ]
      )

      expect(filter).to eq(
        '<div class="filter-control">' \
        '<label for="order-by" class="filter-label">Order By</label>' \
        '<select name="order-by" class="filter-select" ' \
        'data-sorter="viewing-date-desc" data-target="#viewings">' \
        "<option value=\"title-asc\">Title</option>\n" \
        "<option value=\"release-date-desc\">Newest</option>\n" \
        "<option value=\"release-date-asc\">Oldest</option>\n" \
        "<option value=\"viewing-date-desc\">Newest Viewing</option>\n" \
        "<option value=\"viewing-date-asc\">Oldest Viewing</option>\n</select></div>"
      )
    end
  end
end
