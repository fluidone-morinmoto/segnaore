import pytz
#from . import logger
from django.utils import timezone
from django.db import models, transaction


## Abstract Models (providing magic features)

class Timestamps(models.Model):
    class Meta:
        abstract = True

    # date fields
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)

    def save(self, **kw):
        """Automatically set created_at if empty and update
        updated_at field. Keep current values if any error
        occurs while saving.

        """
        msg = "Executing {}.save() ..."
        msg = msg.format(Timestamps().__class__.__name__)
        #logger.debug(msg)

        now = timezone.now()
        current_created_at = self.created_at
        current_updated_at = self.updated_at


        # set created_at only if model has never been saved before
        if not self.id:
            self.created_at = now

        # update_at will always be set to now
        self.updated_at = now

        try:
            with transaction.atomic():
                # call Model save functionality
                super().save(**kw)
        except Exception as e:
            # restore existing values
            self.created_at = current_created_at
            self.updated_at = current_updated_at
            # raise the exception
            raise e

class NoSoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class OnlySoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at=None)


class SoftDelete(models.Model):
    class Meta:
        abstract = True

    # soft delete field
    deleted_at = models.DateTimeField(blank=True, null=True)

    # define managers to retrieve the objects
    objects = NoSoftDeleteManager()
    objects_all = models.Manager()
    objects_deleted = OnlySoftDeleteManager()

    # new behaviour for delete method (set deleted_at field to now)
    def delete(self, **kw):
        """Set deleted_at value to <now> instead of removing
        the record from the databse.

        """
        # define extra once
        extra = {"model": self.__class__.__name__, "id": self.id}

        msg = "Soft-deleting record ..."
        #logger.info(msg, extra=extra)

        current_deleted_at = self.deleted_at
        self.deleted_at = timezone.now()

        try:
            super().save()
        except Exception as e:
            # restore deleted_at (should be None, but maybe it's not)
            self.deleted_at = current_deleted_at
            # raise the exception
            raise e

        # log the success
        msg = "Record successfully soft-deleted"
        #logger.info(msg, extra=extra)

    def restore(self):
        """Restore a soft-deleted model.

        """
        # define extra once
        extra = {"model": self.__class__.__name__, "id": self.id}

        msg = "Restoring soft-deleted record ..."
        #logger.info(msg, extra=extra)

        if self.deleted_at is None:
            msg = "Record seems not to be soft-deleted"
            #logger.info(msg, extra=extra)

        # clean deleted_at field
        self.deleted_at = None
        self.save()

        # log the success
        msg = "Record successfully restored"
        #logger.info(msg, extra=extra)
