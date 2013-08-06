from collections import namedtuple

CHAR_LIMIT = 60.0

def bar_graph(bars):

    # Figure out the highest value
    value_max = 0
    prefix_max = 0

    for bar in bars:

        # Create the prefix for ever bar in the graph
        name = bar['name']
        size = int(bar['num'])

        bar['prefix'] = '{name}: {size} '.format(
            name=name,
            size=size,
        )

        # calculate the maximum prefix size, and bar length
        total = len(bar['prefix']) + int(bar['num'])
        if total > value_max:
            value_max = total
        if len(bar['prefix']) > prefix_max:
            prefix_max = len(bar['prefix'])

    # See if we'll need to scale the bar graph
    if value_max > CHAR_LIMIT:
        ratio = CHAR_LIMIT / value_max
    else:
        ratio = 1

    output_bars = []
    for bar in bars:
        # Pad the line
        line = bar['prefix'] + ' ' * (prefix_max - len(bar['prefix']))

        length = int(bar['num'] * ratio)
        output_bars.append(line + '#' * length)

    out = '\n'.join(output_bars)

    return out


