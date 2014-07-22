``addressable`` is a silly little utility that allows you to access
items inside of a list using one or more indices as keys. You pretty
much get to pretend pretend that a list is a souped-up dictionary.

::

    artists = [{
        'id': '0488', 
        'name': 'Lambchop', 
        'members': ['Kurt Wagner'], 
    }, {
        'id': '9924', 
        'name': 'Dire Straits', 
        'members': ['Mark Knopfler'], 
    }]

    # keys are matched against one or more indices
    artists = List(artists, indices=('id', 'name'))
    print artists['0488'] == artists['Lambchop']

    # fuzzy matching
    artists = List(artists, indices=('id', 'title'), fuzzy=True)
    print artists['strait']

    # extract the value, not the metadata
    artists = List(artists, indices=('id', 'title'), facet='title')
    print artists['9924'] == 'Dire Straits'

So why would you want to do any of this? You probably don't.

``addressable`` can be useful for certain DSL or library code where you
want to give the end users some freedom to code things their way, when
you need to be able to very easily refer to certain things that are
weirdly named or when there's multiple common ways of referring to
something and you want the flexibility to mix-and-match.
