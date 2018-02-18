from django import template
register = template.Library()

# @register.filter(name='cut')
# def cut(value, arg):    # e.g. {{ somevalue|cut:"0" }} 0 is the arg, somevalue is the value
#    """Removes all values of arg from the given string"""
#    return value.replace(arg, '')

# @register.filter
# def lower(value): # Only one argument.
#    """Converts a string into all lowercase"""
#    return value.lower()


@register.inclusion_tag('main/table_two.html')
def kairozu_table2(tableobj):
    if tableobj.header is True:
        return {'title': tableobj.title,
                'tablehead': [tableobj.head_prea, tableobj.head_posta, tableobj.head_note],
                'tabledata': tableobj.twotabledata_set.values_list('f_prea', 'f_posta', 'f_note')}
    else:
        return {'title': tableobj.title,
                'tabledata': tableobj.twotabledata_set.values_list('f_prea', 'f_posta', 'f_note')}


@register.inclusion_tag('main/table_four.html')
def kairozu_table4(tableobj):
    if tableobj.header is True:
        return {'title': tableobj.title,
                'centert': tableobj.center,
                'arrowt': tableobj.arrow,
                'tablehead': [tableobj.head_prea, tableobj.head_preb, tableobj.head_prec, tableobj.head_posta, tableobj.head_postb, tableobj.head_postc],
                'tabledata': tableobj.fourtabledata_set.values_list('f_prea', 'f_preb', 'f_prec', 'f_posta', 'f_postb', 'f_postc')}
    else:
        return {'title': tableobj.title,
                'centert': tableobj.center,
                'arrowt': tableobj.arrow,
                'tabledata': tableobj.fourtabledata_set.values_list('f_prea', 'f_preb', 'f_prec', 'f_posta', 'f_postb', 'f_postc')}


@register.inclusion_tag('main/table_point.html')
def kairozu_point(tableobj):
    return {'lessonid': tableobj.id,
            'grammarnote': tableobj.grammarnote_set.first(),
            'tabledata': tableobj.points.values_list('f_pointa', 'f_pointb')}


@register.inclusion_tag('main/table_summary.html')
def kairozu_summary(tableobj):
    return {'lessonid': tableobj.id,
            'grammarnote': tableobj.grammarnote_set.first(),
            'tabledata': tableobj.points.values_list('f_pointa', 'f_pointb')}
