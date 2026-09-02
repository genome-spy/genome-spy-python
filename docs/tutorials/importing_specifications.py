"""Executable remote-view import used by the user guide."""

# remote-spec-import-start
import genome_spy as gs


SPEC_URL = (
    "https://raw.githubusercontent.com/genome-spy/genome-spy/"
    "d2e9bd71/examples/docs/grammar/composition/layer/"
    "bar-and-label-layer.json"
)

imported_chart = gs.vconcat(gs.import_view(url=SPEC_URL))
# remote-spec-import-end
