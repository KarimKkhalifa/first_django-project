def get_childrent(qs_child):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m%d %H:%m'),
            'is_child': comment.is_child,
            'parent_id': comment.get_parent
        }
        if comment.comment_children:
            c['children'] = get_childrent(comment.comment_children.all())
        res.append(c)
    return res


def create_comments_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m%d %H:%m'),
            'is_child': comment.is_child,
            'parent_id': comment.get_parent
        }
        if comment.comment_children:
            c['children'] = get_childrent(comment.comment_children.all())
        if not comment.is_child:
            res.append(c)
    return res
