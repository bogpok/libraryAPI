def mongo_serialize(mongo_object):
    """ deals with ObjectId
    """
    jobject = {}
    jobject['_id'] = str(mongo_object['_id'])
    del mongo_object['_id']
    jobject.update(**mongo_object)
    return jobject