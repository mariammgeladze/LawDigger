# import mongoengine as moe
from .. import models
from ...data import cache
from .. import law_codes
import logging

logger = logging.getLogger(__name__)

law_code_to_model_map = {
    # law_codes.OREGON_REVISED_STATUTES: {
    #     'statute': models.OregonRevisedStatute,
    #     'volume': models.ORSVolume,
    #     'chapter': models.ORSChapter
    # }
}

float_subsections = ['ors']


# def formatted_subsection(law_code, subsection):
#     if law_code in float_subsections:
#         return float(subsection)
#     else:
#         return subsection


# def fetch_code_version(law_code, version):
#     """Fetch all statutes in code."""
#     model = get_statute_model(law_code)
#     version_key = 'texts.' + str(version)
#     return model.objects(__raw__={
#         version_key: {'$exists': True}
#     })


# def fetch_code_subsections(law_code):
#     cache_key = 'fetch_code_subsections_{}'.format(law_code)
#     cached = cache.get(cache_key)
#     if cached:
#         return cached

#     as_float = False
#     if law_code in ['ors']:
#         as_float = True

#     model = get_statute_model(law_code)
#     subsections = []
#     laws = model.objects.only('subsection').order_by('subsection')
#     for law in laws:
#         if as_float:
#             subsections.append(float(law.subsection))
#         else:
#             subsections.append(law.subsection)
#     subsections.sort()
#     cache.set(cache_key, subsections)
#     return subsections


# def fetch_law(law_code, subsection):
#     model = get_statute_model(law_code)
#     return model.objects(subsection=subsection).first()


# def fetch_ors_by_chapter(chapter):
#     chapter_model = get_chapter_model('ors')
#     chapter = chapter_model.objects(chapter=chapter).first()
#     statute_model = get_statute_model('ors')
#     statutes = statute_model.objects(id__in=chapter.statute_ids)
#     return (chapter, statutes)


# def fetch_previous_and_next_subsections(law_code, subsection):
#     subsection = formatted_subsection(law_code, subsection)
#     subsections = fetch_code_subsections(law_code)
#     max_index = len(subsections) - 1
#     idx = subsections.index(subsection)

#     model = get_statute_model(law_code)
#     if idx > 0:
#         prev = model.subsection_float_to_string(subsections[idx - 1])
#     else:
#         prev = None

#     if idx < max_index:
#         next = model.subsection_float_to_string(subsections[idx + 1])
#     else:
#         next = None

#     return (prev, next)


# def fetch_volumes(law_code):
#     model = get_volume_model(law_code)
#     return model.objects().order_by('volume')


# def get_or_create_volume(volume, law_code):
#     model = get_volume_model(law_code)
#     obj, created = model.objects.get_or_create(volume=volume)
#     return obj


# def get_or_create_chapter(chapter, volume, law_code):
#     model = get_chapter_model(law_code)
#     obj, created = model.objects.get_or_create(
#         chapter=chapter,
#         volume_id=volume.id)
#     return obj


# def get_or_create_law(law_code, subsection):
#     model = get_statute_model(law_code)
#     obj, created = model.objects.get_or_create(subsection=subsection)
#     return obj


# def set_law_version(law, version, title, text):
#     model = models.LawVersion
#     obj, created = model.objects.get_or_create(law_id=law.id)
#     obj.title = title
#     obj.text = text
#     obj.save()
#     return obj


def get_or_create_web_source(url):
    obj, created = models.LawWebSource.objects.get_or_create(url=url)
    return obj


def get_or_create_division(law_code, version, division, parent_id=None):
    version = str(version)
    kwargs = {
        'division': division,
        'law_code': law_code,
        'version': version
    }
    if parent_id:
        kwargs['parent_id'] = parent_id

    obj, created = models.LawDivision.objects.get_or_create(**kwargs)
    if created:
        logger.info('Created LawVersion: {} {} {} (parent: {})'.format(
            version, law_code.upper(), division, obj.parent_id))
    return obj


def create_law_in_division(division, subsection, title, text):
    obj = models.LawVersion(
        division_id=division.id,
        subsection=subsection,
        title=title,
        text=text)
    obj.save()
    return obj

# def fetch_by_code(law_code, version=None):
#     model = get_statute_model(law_code)
#     if not version:
#         return model.objects
#     else:
#         version_key = 'texts.' + str(version)
#         return model.objects(__raw__={
#             version_key: {'$exists': True}
#         })


# def fetch_code_subsections(law_code):
#     cache_key = 'fetch_code_subsections_{}'.format(law_code)
#     cached = cache.get(cache_key)
#     if cached:
#         return cached

#     as_float = False
#     if law_code in ['ors']:
#         as_float = True

#     model = get_statute_model(law_code)
#     subsections = []
#     laws = model.objects.only('subsection').order_by('subsection')
#     for law in laws:
#         if as_float:
#             subsections.append(float(law.subsection))
#         else:
#             subsections.append(law.subsection)
#     subsections.sort()
#     cache.set(cache_key, subsections)
#     return subsections
