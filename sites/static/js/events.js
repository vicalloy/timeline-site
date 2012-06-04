$(function () {
  var tl_tb_body = $('#tl_list table.tllist tbody');
  var save_more = false;//save and add other
  function getMediaType(d) {
    if (d.match("div class='twitter'")) {
      //return "twitter-ready";
      return 'twitter'
    } else if (d.match('(www.)?youtube|youtu\.be')) {
      //return "youtube";
      return "film";
    } else if (d.match('(player.)?vimeo\.com')) {
      //return "vimeo";
      return "film";
    } else if (d.match('(player.)?soundcloud\.com')) {
      //return "soundcloud";
      return "music";
    } else if (d.match('(www.)?twitter\.com')) {
      return "twitter";
    } else if (d.match("maps.google") && !d.match("staticmap")) {
      //return "google-map";
      return "map-marker";
    } else if (d.match("flickr.com/photos")) {
      //return "flickr";
      return "picture";
    } else if (d.match(/jpg|jpeg|png|gif/i) || d.match("staticmap")) {
      //return "image";
      return "picture";
    } else if (d.indexOf('http://') == 0) {
      //return "website";
      return "globe";
    } else {
      return "unknown";
    }
  }
  function safeHtml(s) {
    return $('<div/>').text(s).html().replace(/\n/g, "<br />");
  }
  function genRow(d) {
    d.mediaType = getMediaType(d.media);
    d.title = safeHtml(d.title);
    d.text = safeHtml(d.text);
    d.media = safeHtml(d.media);
    if (d.mediaType == 'picture') {
      d.media = '<img src="' + d.media + '"/>';
    } 
    d.media_caption = safeHtml(d.media_caption);
    return tmpl("events_row_tmpl", d);
  }
  function showForm() {
    $("#insert_tl_img").hide();
    $("#show_tl_img").hide();
    $('#id_title')[0].focus();
    $('#tl_form_div').fadeIn('slow');
    $('.btn_add_event').fadeOut('slow');
    if ($('#id_pk_').val() == '') {
      $('#id_btn_save_more').show();
    } else {
      $('#id_btn_save_more').hide();
    }
    showUploadDiv('.upload');//reload upload img div
    scrollTo(0, $("#tl_form_div").offset().top);
  }
  function hideForm() {
    $('#tl_form_div').fadeOut('slow');
    $('.btn_add_event').fadeIn('slow');
  }
  $('#tl_form').djangoajaxform({
      callback: bootstrapCallback,
      removeErrorHints: bootstrapRemoveErrorHints,
      onValidateSucc: function(data, form){
        if (data.valid) {
          var pk = $('#id_pk_').val();
          if (pk == '') {
            tl_tb_body.append(genRow(data.data));
            initActBtn();
          } else {
            var row = $('#e_' + pk);
            row.fadeOut('slow', function(){
              var nrow = $(genRow(data.data));
              if (nrow.hasClass('cover')) {
                $('tr', tl_tb_body).removeClass('cover');
              }
              row.html(nrow.html()).fadeIn('slow');
              row.attr('class', nrow.attr('class'));
              initActBtn();
            });
          }
          if (save_more) {
            $('#tl_form')[0].reset();
            showUploadDiv('.upload');//reload upload img div
          } else {
            hideForm();
          }
        }
      }
  });

  /*
  $('#id_startdate,#id_enddate').datepicker({
    weekStart: 1,
    format: 'yyyy-mm-dd'
  }).on('changeDate', function(ev){
    $(this).datepicker('hide');
  });*/

  function initActBtn() {
    var del_btns = $(".event .del", tl_tb_body);
    var edit_btns = $(".event .edit", tl_tb_body);
    del_btns.unbind('click')
    edit_btns.unbind('click')
    del_btns.click(function(){
      if (!confirm('确定删除？')) return false;
      var p = $(this).parent().parent();
      var pk = p[0].id.split('_')[1]
      $.getJSON(url_event_delete_, {'pk': pk}, function(data) {
        if (data.valid) {
          p.fadeOut('slow', function(){p.remove()});
        } else {
          alert('删除失败');
        }
      });
    });
    edit_btns.click(function(){
      var p = $(this).parent().parent();
      var pk = p[0].id.split('_')[1]
      $('#id_pk_').val(pk);
      $('#tl_form').attr('action', url_event_edit_ + "?pk=" + pk);
      $('#tl_form_div').fadeOut('slow');
      $.getJSON(url_event_json_, {'pk': pk}, function(data) {
        if (data.valid) {
          formLoadData($('#tl_form'), data.data);
          showForm();
        } else {
          alert('数据加载失败');
        }
      });
    });
  }
  $('.btn_add_event').click(function(){
    $('#id_pk_').val('');
    $('#tl_form').attr('action', url_timeline_addevent_);
    $('#tl_form')[0].reset();
    showForm();
  });
  $('#btn_tlf_cancel').click(function(){
    hideForm();
  });
  $('#id_btn_save_more').click(function(){
    save_more = true;
  });
  $('#id_btn_save').click(function(){
    save_more = false;
  });
  function formLoadData(form, data, field_map, pre) {
    if (pre == undefined) pre = '';
    $.each(data, function(k, v){
      if (v instanceof Object) {
        formLoadData(form, data, field_map, pre + k + '_');
      } else {
        var fid = pre + k;
        if (field_map != undefined)
          var tfid = field_map[fid];
        if (tfid!=undefined) {
          fid = tfid;
        } else {
          fid = 'id_' + fid;
        }
        var f = $('#' + fid, form);
        if (f.attr('type') == 'checkbox') {
          f.attr('checked', v);
        } else {
          $('#' + fid, form).val(v);
        }
      }
    });
  }
  $('textarea').autosize();
  $.getJSON(url_timeline_events_sjson_, {}, function(data) {
    $.each(data, function(i, d){
      tl_tb_body.append(genRow(d));
    });
    initActBtn();
  });
  
  function showSimplePop(btn, pop) {
    pop.css("display", "block");
    pos = $(btn).offset();
    pos["width"] = btn.offsetWidth;
    pos["height"] = btn.offsetHeight;
    actualWidth = pop[0].offsetWidth
    pop.css("top", pos.top + pos.height);
    pop.css("left", pos.left + pos.width / 2 - 80);
  }
  $("#btn_insert_tl_img").click(function(){
    showSimplePop(this, $("#insert_tl_img"));
    $("#show_tl_img").hide();
    $('#insert_tl_img_tab a').first()[0].click();
  });
  $("#btn_show_tl_media").click(function(){
    showSimplePop(this, $("#show_tl_img"));
    $("#insert_tl_img").hide();
    var media = $('#id_media').val();
    if (getMediaType(media) == 'picture') {
      $('#show_tl_img .popover-content').html('<p><img src="' + media + '"/></p>')
    } else {
      $('#show_tl_img .popover-content').html('<p>不支持该类型媒体文件的预览</p>')
    }
  });

  //=============
  function loadTlImg(refresh) {
    if (!refresh && $('#id_tl_imgs').attr('loaded') == '1') {
      return;
    }
    $('#id_tl_imgs ul.thumbnails').html('<p> <img src="{{STATIC_URL}}img/loading.gif" /> 数据加载中，请稍后...  </p>');
    $.get(url_timeline_attachs_, function(data){
      $('#id_tl_imgs ul.thumbnails').html('');
      $.each(data, function (idx, attach) {
        $('#id_tl_imgs ul.thumbnails').append('<li> <a href="###" class="thumbnail"> <img src="' + attach.url + '" alt=""/> </a> </li>');
      });
      $('#id_tl_imgs').attr('loaded', '1');
      $('#id_tl_imgs .thumbnails img').click(function(){
        $('#id_media').val($(this).attr('src'));
        $('#insert_tl_img').hide();
      });
    }, 'json');
  }
  $('#tab_upload_img').click(function(){loadTlImg(false)});
  $('#id_tl_imgs button.refresh').click(function(){loadTlImg(true)});
  $('#insert_tl_img_tab > a').click(function(){
    $('a', $(this).parent()).removeClass('current');
    $(this).addClass('current');
    $('#insert_tl_img .popover-content > div').hide();
    $($(this).attr('href')).show();
    return false;
  });
  var upload = $('#fileupload');
  function showUploadDiv(d) {
    $('.upload, .uploadding, .uimg', upload).hide();
    $(d, upload).show();
  }
  $('.uimg .delete', upload).click(function(){
    var apk = $('.uimg', upload).attr('apk');
    $.post(url_timeline_attach_delete_, {'id': apk}, function(d) {
      if (d.valid) {
        showUploadDiv('.upload');
        $('#id_media').val('');
      } else {
        alert('删除失败');
      }
    }, 'json');
  });

  upload.fileupload();
  upload.fileupload('option', {
      url: url_timeline_attach_upload_,
      autoUpload: true,
      limitMultiFileUploads: 1,
      maxFileSize: 500000,
      acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
  });

  upload
  .bind('fileuploadadd', function (e, data) {
    $.each(data.files, function (index, file) {
      if (file.error) {
        alert(window.locale.fileupload.errors[file.error]);
      }
    });
  })
  .bind('fileuploadsend', function (e, data) {
    showUploadDiv('.uploadding');
  })
  .bind('fileuploaddone', function (e, data) {
    var d = data.result;
    if (d.length>0) {//d.valid
      var a = d[0];
      $('.uimg > p', upload).html('<img src="' + a.url + '"/>');
      $('.uimg', upload).attr('apk', a.id);
      $('#id_media').val(a.url);
      showUploadDiv('.uimg');
    } else {
      showUploadDiv('.upload');
      alert('图片上传失败');
    }
  })
  .bind('fileuploadfail', function (e, data) {
    showUploadDiv('.upload');
    alert('图片上传失败');
  });
});
