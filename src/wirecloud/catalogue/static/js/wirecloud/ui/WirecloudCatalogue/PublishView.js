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

/*global $, Constants, Element, EzWebExt, gettext, interpolate, LayoutManagerFactory, LogManagerFactory, StyledElements, Wirecloud*/

(function () {

    "use strict";

    var PublishView, upload_wgt_file, submit_template;

    /*************************************************************************
     *                            Private methods                            *
     *************************************************************************/

    upload_wgt_file = function upload_wgt_file() {
        LayoutManagerFactory.getInstance()._startComplexTask(gettext("Uploading packaged widget"), 1);
        this.wrapperElement.getElementsByClassName("wgt_upload_form")[0].submit();
    };

    submit_template = function submit_template() {
        var template_uri = this.wrapperElement.getElementsByClassName('template_uri')[0].value;

        LayoutManagerFactory.getInstance()._startComplexTask(gettext("Adding resource to the catalogue"), 1);
        LayoutManagerFactory.getInstance().logSubTask(gettext('Sending resource template to catalogue'));

        this.catalogue.addResourceFromURL(template_uri, {
            forceCreate: true,
            onSuccess: function () {
                LayoutManagerFactory.getInstance().logSubTask(gettext('Resource uploaded successfully'));
                LayoutManagerFactory.getInstance().logStep('');

                this.mainview.home();
                this.mainview.refresh_search_results();
            }.bind(this),
            onFailure: function (msg) {
                LayoutManagerFactory.getInstance().showMessageMenu(msg, Constants.Logging.ERROR_MSG);
            },
            onComplete: function () {
                LayoutManagerFactory.getInstance()._notifyPlatformReady();
            }
        });
        return false;
    };

    /*************************************************************************
     *                              PublishView                              *
     *************************************************************************/

    PublishView = function PublishView(id, options) {
        options.class = 'publish_view';
        this.catalogue = options.catalogue;
        this.mainview = options.mainview;
        StyledElements.Alternative.call(this, id, options);

        var builder = new StyledElements.GUIBuilder();
        var contents = builder.parse($('wirecloud_catalogue_publish_interface').getTextContent(), {
            'back_button': function () {
                var button = new StyledElements.StyledButton({text: gettext('Close upload view')});
                button.addEventListener('click', this.mainview.home.bind(this.mainview));
                return button;
            }.bind(this)
        });
        this.appendChild(contents);

        this.wrapperElement.getElementsByClassName('template_submit_form')[0].onsubmit = submit_template.bind(this);
        this.wrapperElement.getElementsByClassName('upload_wgt_button')[0].addEventListener('click', upload_wgt_file.bind(this), true);

        this.wrapperElement.getElementsByClassName("wgt_upload_form")[0].target = 'upload_' + this.mainview.altId;
        if (this.catalogue.name === 'local') {
            this.wrapperElement.getElementsByClassName("wgt_upload_form")[0].action = Wirecloud.URLs.LOCAL_RESOURCE_COLLECTION;
        } else {
            this.wrapperElement.getElementsByClassName("wgt_upload_form")[0].action = Wirecloud.io.buildProxyURL(this.catalogue.RESOURCE_COLLECTION);
        }
        this._iframe = this.wrapperElement.getElementsByClassName('upload')[0];
        this._iframe.id = this._iframe.name = 'upload_' + this.mainview.altId;
        this._iframe.onload = this._check_upload_wgt_result.bind(this);
    };
    PublishView.prototype = new StyledElements.Alternative();

    PublishView.prototype._check_upload_wgt_result = function () {
        var doc, layoutManager, logManager, msg, processed_response_data;

        if (this._iframe.contentDocument) {
            doc = this._iframe.contentDocument;
        } else if (this._iframe.contentWindow) {
            doc = this._iframe.contentWindow.document;
        } else {
            doc = window.frames.upload.document;
        }

        if (doc.location.href === 'about:blank') {
            return;
        }

        layoutManager = LayoutManagerFactory.getInstance();

        doc.body.getTextContent = Element.prototype.getTextContent;
        if (doc.location.href.search("error") >= 0) {
            logManager = LogManagerFactory.getInstance();
            msg = gettext("The resource could not be added to the catalogue: %(errorMsg)s.");
            msg = interpolate(msg, {errorMsg: doc.body.getTextContent()}, true);

            layoutManager._notifyPlatformReady();
            layoutManager.showMessageMenu(msg, Constants.Logging.ERROR_MSG);
            logManager.log(msg);
        } else {
            layoutManager.logSubTask(gettext('Widget uploaded successfully'));
            layoutManager.logStep('');
            layoutManager._notifyPlatformReady();

            this.mainview.home();
            this.mainview.refresh_search_results();
        }
    };

    Wirecloud.ui.WirecloudCatalogue = {};
    Wirecloud.ui.WirecloudCatalogue.PublishView = PublishView;
})();