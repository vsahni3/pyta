import astroid
import nose
from hypothesis import settings, given
from typing import Dict
import tests.custom_hypothesis_support as cs
settings.load_profile("pyta")


@given(cs.homogeneous_dictionary(min_size=1))
def test_dict_comprehension_reproduce_homogeneous(dictionary):
    """Test DictComp node visitor representing a comprehension expression reproducing the the key, value pairs
    of a homogeneous Dictionary."""
    program = f"a = {{key: {dictionary}[key] for key in {dictionary}}}"
    module, TypeInferrer = cs._parse_text(program)
    dictcomp_node = list(module.nodes_of_class(astroid.DictComp))[0]
    # reproducing the dict with dict. comprehension; the type of the expression will be same as original iterable
    assert dictcomp_node.type_constraints.type == dictcomp_node.generators[0].iter.type_constraints.type


@given(cs.heterogeneous_dictionary(min_size=1))
def test_dict_comprehension_reproduce_heterogeneous(dictionary):
    """Test DictComp node visitor representing a comprehension expression reproducing the the key, value pairs
    of a heterogeneous Dictionary."""
    program = f"a = {{key: {dictionary}[key] for key in {dictionary}}}"
    module, TypeInferrer = cs._parse_text(program)
    dictcomp_node = list(module.nodes_of_class(astroid.DictComp))[0]
    assert dictcomp_node.type_constraints.type == dictcomp_node.generators[0].iter.type_constraints.type


if __name__ == '__main__':
    nose.main()
