from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset 
from pylexibank import Language, FormSpec
from pylexibank import progressbar

from clldutils.misc import slug
import attr


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "duonglachi"
    writer_options = dict(keep_languages=False, keep_parameters=False)
    form_spec = FormSpec(
            missing_data=("---", '33', ),
            separators="/,",
            replacements=[(" ", "_"), (" ", "_")]
            )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            cid = '{0}_{1}'.format(concept.number, slug(concept.english))
            args.writer.add_concept(
                    ID=cid,
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss
                    )
            concepts[concept.english] = cid
        languages = args.writer.add_languages(lookup_factory="Name")
        args.writer.add_sources()

        for row in self.raw_dir.read_csv('data.tsv', delimiter='\t',
                dicts=True):
            cid = concepts[row['English'].strip()]
            for language, lid in languages.items():
                form = row[language]
                if form and form != '---':
                    args.writer.add_forms_from_value(
                            Language_ID=lid,
                            Parameter_ID=cid,
                            Value=form,
                            Source='Duong2020'
                            )


