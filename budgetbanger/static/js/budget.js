undoneTemplate = '<li><span class="handle"> :: </span> <input type="text" class="listItem form-control" value="{{value}}">' +
  '<a class="checkListItem" style="display: inline;" href="#"><i class="fa fa-square-o fa-2x"></i></a>' +
  '<a class="removeListItem" style="display: inline;" href="#"> <i class="fa fa-times fa-2x"></i></a></li>';
doneTemplate = '<li><span class="handle"> :: </span> <input type="text" class="listItem form-control" value="{{value}}">' +
  '<a class="checkListItem" style="display: inline;" href="#"><i class="fa fa-check-square-o fa-2x"></i></a>' +
  '<a class="removeListItem" style="display: inline;" href="#"> <i class="fa fa-times fa-2x"></i></a></li>';


function loadToDo() {
  var list = $("#theList");
  var jsonData = "";
  $.ajax({
    type:"GET",
    url: "/ajax",
    success: function(data) {
      $("#anyad").text(data);
      $.each(data.todo, function (i, obj) {
        if (obj.checked == 'true') {
          list.append(Mustache.render(doneTemplate,obj))
        } else {
          list.append(Mustache.render(undoneTemplate, obj))
        }
      });

      $(".sortable").sortable("destroy");
      $(".sortable").sortable({
        handle: ".handle"
      });
      var theCount = $("#theList li").length + 1;
      if (theCount > 1) {
        $("#doClearAll").css("display", "block");
      }
    },
    error: function() {
      alert("There was a problem during the first GET request of the ToDo List");
    }
  });
}

function update () {
  var list = $("#theList li");
  var data = {"todo": []};

  list.each(function(idx, li) {
    var todo = $(li);
    var text = todo.find(".listItem").val();
    var checked = todo.hasClass("done");
    data["todo"].push({"id": idx,
                       "value": text,
                       "checked": checked});
  });
  $.ajax({
    type:"POST",
    dataType : "json",
    contentType: "application/json; charset=utf-8",
    url: "/todo_json",
    data: JSON.stringify(data),
    success: function(data) {
      console.log("success", data);
      $("#anyad").text(JSON.stringify(data));
    },
    error: function() {
      alert("Something is screwed up with ajax");
    }
  });
}


function expenditure_loadToDo() {
  var list = $("#expenditure_theList");
  var jsonData = "";
  $.ajax({
    type:"GET",
    url: "/ajax",
    success: function(data) {
      $.each(data.todo, function (i, obj) {
        if (obj.checked == 'true') {
          list.append(Mustache.render(doneTemplate,obj))
        } else {
          list.append(Mustache.render(undoneTemplate, obj))
        }
      });

      $(".sortable").sortable("destroy");
      $(".sortable").sortable({
        handle: ".handle"
      });
      var theCount = $("#expenditure_theList li").length + 1;
      if (theCount > 1) {
        $("#expenditure_doClearAll").css("display", "block");
      }
    },
    error: function() {
      alert("There was a problem during the first GET request of the ToDo List");
    }
  });
}

function expenditure_update () {
  var list = $("#expenditure_theList li");
  var data = {"todo": []};

  list.each(function(idx, li) {
    var todo = $(li);
    var text = todo.find(".listItem").val();
    var checked = todo.hasClass("done");
    data["todo"].push({"id": idx,
                       "value": text,
                       "checked": checked});
  });
  $.ajax({
    type:"POST",
    dataType : "json",
    contentType: "application/json; charset=utf-8",
    url: "/todo_json",
    data: JSON.stringify(data),
    success: function(data) {
      console.log("success", data);
    },
    error: function() {
      alert("Something is screwed up with ajax");
    }
  });
}




$(document).ready(function () {


  var newListItem;
  var newList = true;
  var theList = document.getElementById('theList');
  $("#doClearAll").css("display", "none");


  $('#addToDo').on("click", function(e) {
    e.preventDefault(); //Prevent the default functionality of the button
    if (newList == true) {
      var theValue = $("#item").val();
      newListItem = '<li><span class="handle"> :: </span> <input type="text" class="listItem form-control" value="' +theValue + '">' +
        '<a class="checkListItem" style="display: inline;" href="#"><i class="fa fa-square-o fa-2x"></i></a>' +
        '<a class="removeListItem" style="display: inline;" href="#"> <i class="fa fa-times fa-2x"></i></a></li>';
      newList = false;

    } else {
      var theValue = $("#item").val();
      newListItem = $("#theList li:last").clone();
      newListItem.find("input").attr("value", theValue);
      if (newListItem.hasClass("done")) {
        newListItem.removeClass("done");
      }
    }



    $("#theList").append(newListItem);

    var theCount = $("#theList li").length + 1;
    if (theCount > 1) {
      $("#doClearAll").css("display", "block");
    }

    $("#item").val("");
    $("#item").focus();
    $(".sortable").sortable("destroy");
    $(".sortable").sortable({
      handle: ".handle"
    });
    update();

  });


  $('#item').on("keydown", function(e) {
    var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
    if (key == 13) {
      e.preventDefault();
      var inputs = $(this).closest("form").find(":input:visible");
      inputs.eq(inputs.index(this) + 1).click();
    }
  });


  $("#theList").on("change", ".listItem", function(e) {
    var currentValue = $(this).val();
    $(this).attr("value", currentValue);

    update();

  });


  $(".sortable").sortable().bind("sortupdate", function() {

    update();

  });


  $("#theList").on("click", ".checkListItem", function(e) {
    e.preventDefault();
    var a_tag = $(this).parent();
    if (a_tag.hasClass('done')) {
      a_tag.removeClass("done");
      $(this).children('i').removeClass('fa-check-square-o').addClass('fa-square-o');
    } else {
      a_tag.addClass("done");
      $(this).children('i').removeClass('fa-square-o').addClass('fa-check-square-o');
    }

    update();

  });


  $("#theList").on("click", ".removeListItem", function (e) {
    e.preventDefault();
    $(this).parent().remove();
    if ($("#theList li").length == 0) {
      newList = true;
      $("#doClearAll").css("display", "none");
    }

    update();

  });


  $("#doClearAll").on("click", function (e) {
    e.preventDefault();
    $("#theList").children().remove();
    newList = true;
    $("#item").val("");
    $("#doClearAll").css("display", "none");
    $("#item").focus();
    update();
  });


  var newListItem;
  var newList = true;
  var expenditure_theList = document.getElementById('expenditure_theList');
  $("#expenditure_doClearAll").css("display", "none");


  $('#expenditure_addToDo').on("click", function(e) {
    e.preventDefault(); //Prevent the default functionality of the button
    if (newList == true) {
      var theValue = $("#expenditure_item").val();
      newListItem = '<li><span class="handle"> :: </span> <input type="text" class="listItem form-control" value="' +theValue + '">' +
        '<a class="checkListItem" style="display: inline;" href="#"><i class="fa fa-square-o fa-2x"></i></a>' +
        '<a class="removeListItem" style="display: inline;" href="#"> <i class="fa fa-times fa-2x"></i></a></li>';
      newList = false;

    } else {
      var theValue = $("#expenditure_item").val();
      newListItem = $("#expenditure_theList li:last").clone();
      newListItem.find("input").attr("value", theValue);
      if (newListItem.hasClass("done")) {
        newListItem.removeClass("done");
      }
    }



    $("#expenditure_theList").append(newListItem);

    var theCount = $("#expenditure_theList li").length + 1;
    if (theCount > 1) {
      $("#expenditure_doClearAll").css("display", "block");
    }

    $("#expenditure_item").val("");
    $("#expenditure_item").focus();
    $(".sortable").sortable("destroy");
    $(".sortable").sortable({
      handle: ".handle"
    });
    expenditure_update();

  });


  $('#expenditure_item').on("keydown", function(e) {
    var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
    if (key == 13) {
      e.preventDefault();
      var inputs = $(this).closest("form").find(":input:visible");
      inputs.eq(inputs.index(this) + 1).click();
    }
  });


  $("#expenditure_theList").on("change", ".listItem", function(e) {
    var currentValue = $(this).val();
    $(this).attr("value", currentValue);

    expenditure_update();

  });


  $(".sortable").sortable().bind("sortupdate", function() {

    expenditure_update();

  });


  $("#expenditure_theList").on("click", ".checkListItem", function(e) {
    e.preventDefault();
    var a_tag = $(this).parent();
    if (a_tag.hasClass('done')) {
      a_tag.removeClass("done");
      $(this).children('i').removeClass('fa-check-square-o').addClass('fa-square-o');
    } else {
      a_tag.addClass("done");
      $(this).children('i').removeClass('fa-square-o').addClass('fa-check-square-o');
    }

    expenditure_update();

  });


  $("#expenditure_theList").on("click", ".removeListItem", function (e) {
    e.preventDefault();
    $(this).parent().remove();
    if ($("#expenditure_theList li").length == 0) {
      newList = true;
      $("#expenditure_doClearAll").css("display", "none");
    }

    expenditure_update();

  });


  $("#expenditure_doClearAll").on("click", function (e) {
    e.preventDefault();
    $("#expenditure_theList").children().remove();
    newList = true;
    $("#expenditure_item").val("");
    $("#expenditure_doClearAll").css("display", "none");
    $("#expenditure_item").focus();
    expenditure_update();
  });

  loadToDo();
  expenditure_loadToDo();


});