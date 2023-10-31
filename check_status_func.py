def check_status(old_list, new_list):
    old_dict = {obj.id: obj for obj in old_list}
    new_dict = {obj.id: obj for obj in new_list}

    all_objects_dict = {obj.id: obj for obj in old_list + new_list}
    all_objects = sorted(list(all_objects_dict.values()),
                         key=lambda obj: obj.id)

    added_objects = [new_dict[id]
                     for id in (set(new_dict.keys()) - set(old_dict.keys()))]

    deleted_objects = [old_dict[id]
                       for id in (set(old_dict.keys()) - set(new_dict.keys()))]

    modified_objects = [new_dict[id] for id in set(old_dict.keys()) & set(new_dict.keys())
                        if new_dict[id].code != old_dict[id].code
                        or new_dict[id].name != old_dict[id].name]

    return all_objects, added_objects, deleted_objects, modified_objects
