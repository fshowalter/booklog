# frozen_string_literal: true
require 'spec_helper'

describe Booklog::Book do
  let(:book) do
    Booklog::Book.new(
      title: 'The Shining',
      aka_titles: [],
      authors: ['King, Stephen'],
      page_count: '447',
      year_published: '1977',
      isbn: '1234567890'
    )
  end

  describe '#sortable_title' do
    it 'returns a sortable title' do
      expect(book.sortable_title).to eq('Shining, The')
    end

    describe 'when title is already sortable' do
      let(:book) do
        Booklog::Book.new(
          title: 'Night Shift',
          aka_titles: [],
          authors: ['King, Stephen'],
          page_count: '326',
          year_published: '1978',
          isbn: '0987654321'
        )
      end

      it 'returns title' do
        expect(book.sortable_title).to eq('Night Shift')
      end
    end
  end

  describe '#title_with_author' do
    it 'returns the title with author' do
      expect(book.title_with_author).to eq('The Shining by Stephen King')
    end
  end
end
