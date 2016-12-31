# frozen_string_literal: true
require 'spec_helper'
require 'support/stub_template_context'

describe Movielog::Helpers do
  let(:context) { stub_template_context }
  describe '#text_filter' do
    it 'returns a javascript range filter' do
      filter = context.text_filter(
        label: 'Title',
        placeholder: 'Search Titles',
        attribute: 'data-title'
      )
      expect(filter).to eq(
        '<div class="filter-control">' \
        '<label for="title" class="filter-label">Title</label>' \
        '<div class="filter-text_box_wrap">' \
        '<input type="text" name="title" ' \
        'placeholder="Search Titles" class="filter-text_box" ' \
        'data-filter-attribute="data-title" data-filter-type="text" /></div></div>'
      )
    end
  end
end
