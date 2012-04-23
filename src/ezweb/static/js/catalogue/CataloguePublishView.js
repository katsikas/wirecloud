/*
 *     (C) Copyright 2012 Universidad Politécnica de Madrid
 *
 *     This file is part of Wirecloud Platform.
 *
 *     Wirecloud Platform is free software: you can redistribute it and/or
 *     modify it under the terms of the GNU Affero General Public License as
 *     published by the Free Software Foundation, either version 3 of the
 *     License, or (at your option) any later version.
 *
 *     Wirecloud is distributed in the hope that it will be useful, but WITHOUT
 *     ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 *     FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
 *     License for more details.
 *
 *     You should have received a copy of the GNU Affero General Public License
 *     along with Wirecloud Platform.  If not, see
 *     <http://www.gnu.org/licenses/>.
 *
 */

/*jshint forin:true, eqnull:true, noarg:true, noempty:true, eqeqeq:true, bitwise:true, undef:true, curly:true, browser:true, indent:4, maxerr:50, prototypejs: true */
/*global EzWebExt, gettext, StyledElements*/

var CataloguePublishView = function (id, options) {
    options.class = 'publish_view';
    this.catalogue = options.catalogue;
    StyledElements.Alternative.call(this, id, options);

    this.wrapperElement.innerHTML = $('wirecloud_catalogue_publish_interface').getTextContent();

    this.wrapperElement.getElementsByClassName('template_submit_form')[0].onsubmit = this._submit_template.bind(this);
    this.wrapperElement.getElementsByClassName('back_to_resource_list')[0].addEventListener('click', this.catalogue.home.bind(this.catalogue));

    // TODO
    setTimeout(function () {
        $('upload_wgt_button').addEventListener('click', this._upload_wgt_file.bind(this), true);
        $('upload').onload = this._check_upload_wgt_result.bind(this);
    }.bind(this), 0);
};
CataloguePublishView.prototype = new StyledElements.Alternative();

CataloguePublishView.prototype._upload_wgt_file = function () {
    LayoutManagerFactory.getInstance()._startComplexTask(gettext("Uploading packaged gadget"), 1);
    this.wrapperElement.getElementsByClassName("wgt_upload_form")[0].submit();
};

CataloguePublishView.prototype._submit_template = function (e) {
    var template_uri = this.wrapperElement.getElementsByClassName('template_uri')[0].value;

    LayoutManagerFactory.getInstance()._startComplexTask(gettext("Adding resource to the catalogue"), 1);
    LayoutManagerFactory.getInstance().logSubTask(gettext('Sending resource template to catalogue'));

    Wirecloud.io.makeRequest(URIs.GET_POST_RESOURCES, {
        method: 'POST',
        parameters: {'template_uri': template_uri},
        onSuccess: function (transport) {
            LayoutManagerFactory.getInstance().logSubTask(gettext('Resource uploaded successfully'));
            LayoutManagerFactory.getInstance().logStep('');

            this.catalogue.home();
            this.catalogue.refresh_search_results();
        }.bind(this),
        onFailure: function (transport) {
            var msg = LogManagerFactory.getInstance().formatError(gettext("Error uploading resource: %(errorMsg)s."), transport);
            LogManagerFactory.getInstance().log(msg);
            LayoutManagerFactory.getInstance().showMessageMenu(msg, Constants.Logging.ERROR_MSG);
            LayoutManagerFactory.getInstance().log(msg);
        },
        onComplete: function () {
            LayoutManagerFactory.getInstance()._notifyPlatformReady();
        }
    });
    return false;
};

CataloguePublishView.prototype._check_upload_wgt_result = function () {
    var iframe, doc, layoutManager, logManager, msg, processed_response_data;

    iframe = document.getElementById("upload");

    if (iframe.contentDocument) {
        doc = iframe.contentDocument;
    } else if (iframe.contentWindow) {
        doc = iframe.contentWindow.document;
    } else {
        doc = window.frames.upload.document;
    }

    layoutManager = LayoutManagerFactory.getInstance();

    doc.body.getTextContent = Element.prototype.getTextContent;
    if (doc.location.href.search("error") >= 0) {
        logManager = LogManagerFactory.getInstance();
        msg = gettext("The resource could not be added to the catalogue: %(errorMsg)s");
        msg = interpolate(msg, {errorMsg: doc.body.getTextContent()}, true);

        layoutManager._notifyPlatformReady();
        layoutManager.showMessageMenu(msg, Constants.Logging.ERROR_MSG);
        logManager.log(msg);
    } else {
        layoutManager.logSubTask(gettext('Gadget uploaded successfully'));
        layoutManager.logStep('');
        layoutManager._notifyPlatformReady();

        this.catalogue.home();
        this.catalogue.refresh_search_results();
    }
};