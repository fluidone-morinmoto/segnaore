"""
Define custom log stuff.

"""

import copy
import logging
import json
from pythonjsonlogger.jsonlogger import JsonFormatter

class DatabaseLogHandler(logging.Handler):

    def emit(self, record):
        from .models import Log

        msg = self.format(record)
        project_id = None
        json_msg = {}
        try:
            json_msg = json.loads(msg)
            project_id = json_msg.get('project_id')
        except ValueError as e:
            logmsg = "msg is not in correct json format {}".format(msg)
            logger.warning(logmsg)
        kwargs = {
            'level': record.levelno,
            'msg': msg,
            'project_id': project_id
        }

        Log.objects.create(**kwargs)


class JsonInMessageFormatter(JsonFormatter):
    """This formatter embeds the json as the tail of the message
    attribute preserving in this way the record original format.

    """
    def __init__(self, *args, **kwargs):
        self.msg_in_json = kwargs.pop('msg_in_json', False)
        super().__init__(*args, **kwargs)

    def format(self, record):
        # get the json from its parent
        json_record = super().format(record)
        # remove the 'message' attribute
        additional = {}
        #if not self.msg_in_json:
        decoded = json.loads(json_record)
        project_id = decoded.pop('project_id', None)
        if project_id is not None:
            additional['project_id'] = project_id
        project_name = decoded.pop('project_name', None)
        if project_name is not None:
            additional['project_name'] = project_name
        stage = decoded.pop('stage', None)
        if stage is not None:
            additional['stage'] = stage


        # perform a deep copy in order not to affect the original
        # log record which will be passed to other handlers
        record_copy = copy.deepcopy(record)
        #record_copy.msg = "{} {}".format(record.getMessage(), json_record)

        final_msg = "{}".format(record.getMessage())
        if len(additional) != 0:
            json_additional = json.dumps(additional)
            print("------------------------------------- ")
            print(json_additional)
            final_msg += " || {}"
            final_msg = final_msg.format(json_additional)

        record_copy.msg = final_msg
        return logging.Formatter.format(self, record_copy)


class ContentHistoryJsonFilter(logging.Filter):
    """Filter just the logrecords which refers to files, FlexiCapture
    records or Documents.

    """
    def filter(self, log_record):
        # keep the log record if there is at least one of this property
        searching = [
            'filepath',
            'input_file_id',
            'record_id',
            'output_document_id',
            'exportable_document_id',
        ]
        for key in searching:
            if getattr(log_record, key, None) is not None: return True

        # refuse everything else
        return False
