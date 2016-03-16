window.onload = function() {
        $(function() {
          var a11ypi = {
            auth : " ",
            loc:" ",
            elementTagName: " ",
            elementId: " ",
            flag : 0,
            fflag  : 0,
            showbox : 0,
            showlinks : 0,
            blog_flag: false,
            target : false,
            pageHtml:'',
            d: {},
            responseJSON:'',
           
            loadOverlay: function()
            {
            alert('hello');
        		  var overlay_template = '<div id="renarrated_overlay" class="alipi ui-widget-header ui-corner-all">'+
                '<button id="outter-down-button" class="alipi" onclick="a11ypi.outterToggle();" up="true" title="Move this bar to top">Move</button> '+
	              '<button id="outter-up-button" class="alipi" onclick="a11ypi.outterToggle();" title="Move this bar to bottom">Move</button> '+
	              '<button id="edit-current" class="alipi" title="Allow to edit this page">Re-narrate</button> '+
	              '<button id="see-narration" class="alipi" title="See other renarrations, which are in same or other languages"> '+
	                  'Re-narrations</button>'+
	              // '<button id="see-comment" class="alipi" onclick="a11ypi.showComment();" title="5el"> '+
	              // '5el</button>'+
                '<button id="see-links" class="alipi"  title="See other re-narrated pages of this domain">Re-narrated Pages '+
	                  '</button>'+
                    '<button id="alipi-login" class="alipi" onclick="a11ypi.login();" title="Login to SWeeT store">Login</button>'+
                // '<select id="blog-filter" class="alipi" onChange="a11ypi.checkSelect();" title="Select one of the blog name"></select>'+
                '<button id="go" class="alipi ui-icon-circle-arrow-e" onclick="a11ypi.go();" title="Filter by blog" >|Y|</button>'+
                '<div id="show-box" title="Choose a narration"></div> '+
	              '<div id="show-comment" title="Comments for"></div> '+
	              '<div id="show-links" title="List of pages narrated in this domain" class="alipi"></div> '+
	              '<div id="share-box" class="alipi" title="Share this page in any following social network"></div>';

		          var pub_overlay_template = '<div id="pub_overlay" class="alipi ui-widget-header ui-corner-all">'+
	              '<button id="icon-up" class="alipi" down="true" onClick="a11ypi.hide_overlays();" title="Move this bar to top">Move</button>'+ //&#x25B2
	              '<button id="icon-down" class="alipi" onClick="a11ypi.hide_overlays();" title="Move this bar to bottom">Move</button>'+ //&#x25BC
	              '<button id="exit-mode" class="alipi" onclick="a11ypi.exitMode();" title="Do not want to save any changes, just take me out of this editing"> '+
	              'Exit</button>'+
                '<button id="help-window" class="alipi" onclick="a11ypi.help_window();" title="How may I help you in editing this page?">Help</button>'+
                '<button id="undo-button" class="alipi" onclick="a11ypi.util.undoChanges();"title="Undo previous change, one by one">Undo changes</button>'+
                '<button id="publish-button" class="alipi" onclick="a11ypi.loginToSwtStore();"title="Publish your changes to blog">Publish</button></div>';

              var element_edit_overlay_template = '<div id="element_edit_overlay" class="alipi ui-widget-header ui-corner-all" >'+
					          '<button id="edit-text" class="alipi" onclick="a11ypi.displayEditor();" title="Help you to edit this element by providing an editor on right'+
	              ' & reference on left.">Edit Text</button>'+
                '<button id="add-audio" class="alipi" onclick="a11ypi.addAudio();" title="Allow you to give an audio file(.ogg) link to add your audio '+
	              'to this element ">Add Audio</button>'+
                '<button id="replace-image" class="alipi" onclick="a11ypi.imageReplacer();" title="Allow you to give an image file(jpeg/jpg/gif/png) '+
	              'link to replace with this image">Replace Image</button>'+
	              '<button id="delete-image" class="alipi" onclick="pageEditor.deleteImage();" title="Remove this image from page">Delete Image</button>'+
	              '<button id="close-element" class="alipi" onclick="pageEditor.cleanUp();" title="Close" ></button>'+
	              '<label id="cant-edit" class="alipi">No selection / Too large selection </label> '+
	              '</div>';

		          $('body').append(overlay_template);
		          $('body').append(pub_overlay_template);
		          $('body').append(element_edit_overlay_template);

		          $('#outter-up-button').show();
		          $('#go').button({disabled : true});
		          $('#undo-button').button({ disabled: true});
		          $('#publish-button').button({ disabled: true});


		          $("#outter-down-button").button({icons:{primary:"ui-icon-circle-arrow-n"},text:false});  $('#outter-down-button').children().addClass('alipi');
		          $("#outter-up-button").button({icons:{primary:"ui-icon-circle-arrow-s"},text:false});  $('#outter-up-button').children().addClass('alipi');
		          $("#edit-current").button({icons:{primary:"ui-icon-pencil"}});  $('#edit-current').children().addClass('alipi');
		          $("#see-narration").button({icons:{primary:"ui-icon-document-b"}});  $('#see-narration').children().addClass('alipi');
		          $("#see-comment").button({icons:{primary:"ui-icon-document-b"}});  $('#see-comment').children().addClass('alipi');
		          $("#see-links").button({icons:{primary:"ui-icon-link"}});  $('#see-links').children().addClass('alipi');
		          /*$("#blog-filter").button({icons:{secondary:"ui-icon-triangle-1-s"}}); */ $('#blog-filter').children().addClass('alipi');
		          $("#go").button({icons:{primary:"ui-icon-arrowthick-1-e"},text:false});  $('#go').children().addClass('alipi');
		          $("#share").button({icons:{primary:"ui-icon-signal-diag"}});  $('#share').children().addClass('alipi');
		          $("#orig-button").button({icons:{primary:"ui-icon-extlink"}});  $('#orig-button').children().addClass('alipi');
		          $("#info").button({icons:{primary:"ui-icon-info"}});  $('#info').children().addClass('alipi');

		          $("#icon-up").button({icons:{primary:"ui-icon-circle-arrow-n"},text:false});  $('#icon-up').children().addClass('alipi');
		          $("#icon-down").button({icons:{primary:"ui-icon-circle-arrow-s"},text:false});  $('#icon-down').children().addClass('alipi');
		          $("#exit-mode").button({icons:{primary:"ui-icon-power"}});  $('#exit-mode').children().addClass('alipi');
		          $("#help-window").button({icons:{primary:"ui-icon-help"}});  $('#help-window').children().addClass('alipi');
		          $("#undo-button").button({icons:{primary:"ui-icon-arrowreturnthick-1-w"}});  $('#undo-button').children().addClass('alipi');
		          $("#publish-button").button({icons:{primary:"ui-icon-circle-check"}});  $('#publish-button').children().addClass('alipi');

		          $("#edit-text").button({icons:{primary:"ui-icon-pencil"}});   $('#edit-text').children().addClass('alipi');
		          $("#add-audio").button({icons:{primary:"ui-icon-circle-plus"}}); $('#add-audio').children().addClass('alipi');
		          $("#replace-image").button({icons:{primary:"ui-icon-transferthick-e-w"}}); $('#replace-image').children().addClass('alipi');
		          $("#delete-image").button({icons:{primary:"ui-icon-trash"}}); $('#delete-image').children().addClass('alipi');
		          $("#close-element").button({icons:{primary:"ui-icon-circle-close"},text:false}); $("#close-element").children().addClass('alipi');
}
            
          };
          window.a11ypi = a11ypi;


        });
        window.a11ypi.loadOverlay();
        window.a11ypi.ren();
    };
