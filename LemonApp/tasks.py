from __future__ import absolute_import

from django.conf import settings
from LemonApp.models import PPTList

if not settings.DEBUG:
    from celery import shared_task
    
    @shared_task
    def ppt_to_img(ppt_path, ppt_pk):
        img_dir = os.path.join(os.path.split(ppt_path)[0], os.path.splitext(os.path.split(ppt_path)[1])[0])
        pdf_path = os.path.join(img_dir, os.path.splitext(os.path.split(ppt_path)[1])[0] + ".pdf")
        if not os.path.exists(img_dir):
            os.mkdir(img_dir)
        if os.system("unoconv -f %s -o %s %s" % ("pdf", pdf_path, ppt_path)):
            raise RuntimeError("unoconv error")
        if(os.system("convert -density 250 %s -quality 70 %s" % (pdf_path, os.path.join(img_dir, "%d.jpg")))):
            raise RuntimeError("convert error")
        ppt = PPTList.objects.filter(pk=ppt_pk)[0]
        ppt.page_count = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))]) - 1
        ppt.save()