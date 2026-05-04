import src.data.species.pkmn_types as t

def test_getComponentTypes_simple() -> None:
    typeCode = 6
    expected = (2, 3)
    result = t.getComponentTypes(typeCode)
    assert result == expected

def test_getComponentTypes_impossibleTypeCode() -> None:
    typeCode = 12
    expected = -1
    result = t.getComponentTypes(typeCode)
    assert result == expected

def test_getComponentTypes_impossiblePrime() -> None:
    typeCode = 113 * 2 #113 is the 30th prime, but there are only 19 types
    expected = -1
    result = t.getComponentTypes(typeCode)
    assert result == expected