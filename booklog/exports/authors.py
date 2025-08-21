
from booklog.exports import exporter, json_work_author, utils
from booklog.exports.json_author_with_reviewed_works import JsonAuthorWithReviewedWorks
from booklog.exports.json_reviewed_work import JsonReviewedWork
from booklog.exports.repository_data import RepositoryData
from booklog.repository import api as repository_api
from booklog.utils.logging import logger


def _build_work_sequence(
    work: repository_api.Work, repository_data: RepositoryData
) -> str:
    first_author_sort_name = ""
    if work.work_authors:
        first_author = work.work_authors[0].author(repository_data.authors)
        first_author_sort_name = first_author.sort_name
    return f"{work.year}-{first_author_sort_name}-{work.sort_title}"


def _build_author_sequence(
    work: repository_api.Work, repository_data: RepositoryData
) -> str:
    first_author_sort_name = ""
    if work.work_authors:
        first_author = work.work_authors[0].author(repository_data.authors)
        first_author_sort_name = first_author.sort_name
    return f"{first_author_sort_name}-{work.year}-{work.sort_title}"


def _build_title_sequence(
    work: repository_api.Work, repository_data: RepositoryData
) -> str:
    first_author_sort_name = ""
    if work.work_authors:
        first_author = work.work_authors[0].author(repository_data.authors)
        first_author_sort_name = first_author.sort_name
    return f"{work.sort_title}-{first_author_sort_name}-{work.year}"


def _build_json_author_reviewed_work(
    work: repository_api.Work,
    review: repository_api.Review,
    repository_data: RepositoryData,
) -> JsonReviewedWork:
    review_sequence = utils.build_review_sequence(review, repository_data)

    return JsonReviewedWork(
        reviewSequence=review_sequence,
        title=work.title,
        subtitle=work.subtitle,
        workYear=work.year,
        workYearSequence=_build_work_sequence(work, repository_data),
        authorSequence=_build_author_sequence(work, repository_data),
        titleSequence=_build_title_sequence(work, repository_data),
        kind=work.kind,
        slug=work.slug,
        sortTitle=work.sort_title,
        grade=review.grade,
        gradeValue=review.grade_value,
        reviewDate=review.date,
        yearReviewed=review.date.year,
        authors=[
            json_work_author.build_json_work_author(
                work_author=work_author, all_authors=repository_data.authors
            )
            for work_author in work.work_authors
        ],
        includedInSlugs=[work.slug for work in work.included_in_works(repository_data.works)],
    )


def _build_json_author(
    author: repository_api.Author, repository_data: RepositoryData
) -> JsonAuthorWithReviewedWorks:
    author_works = list(author.works(repository_data.works))

    reviewed_works = []

    for work in author_works:
        review = work.review(repository_data.reviews)
        if review:
            reviewed_works.append(
                _build_json_author_reviewed_work(
                    work=work, review=review, repository_data=repository_data
                )
            )

    return JsonAuthorWithReviewedWorks(
        name=author.name,
        sortName=author.sort_name,
        slug=author.slug,
        reviewedWorks=reviewed_works,
    )


def export(repository_data: RepositoryData) -> None:
    logger.log("==== Begin exporting {}...", "authors")

    json_authors = [
        _build_json_author(
            author=author,
            repository_data=repository_data,
        )
        for author in repository_data.authors
    ]

    exporter.serialize_dicts_to_folder(
        [json_author for json_author in json_authors if len(json_author["reviewedWorks"]) > 0],
        "authors",
        filename_key=lambda json_author: json_author["slug"],
    )
