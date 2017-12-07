
// login = document.getElementById("login");
// login.onclick = showForm;

var login = document.getElementById("login");

function showForm(event) {
        // alert(form);
        var parameters = "form_login";

         $.getJSON(Flask.url_for("login"), parameters)
        .done(function(data, textStatus, jqXHR) {

             count_filds = 3;

             for (var i = 0; i < count_filds; i++)
             {
                     consol.log(data[1]);
             }
      })
      .fail(function(jqXHR, textStatus, errorThrown) {

            // log error to browser's console
            console.log(errorThrown.toString());
        });

}

// function initElement() {


//          showForm(login.onclick);
//       };

// initElement();

// document.event.addListener(marker, 'click', function() {

//         $.getJSON(Flask.url_for("articles"), parameters)
//         .done(function(data, textStatus, jqXHR) {

//             count_news = 5;

//             content = "<ul>";
//            // add new markers to map
//            for (var i = 0; i < count_news; i++)
//            {
//             content += "<li><a target=&#039_blank" + "&#039 href=" + data[i]["link"] + ">" + data[i]["title"] + "</a></li>";
//            }
//            content += "</ul>";

//            showInfo(marker, content);
//         })
//         .fail(function(jqXHR, textStatus, errorThrown) {

//             // log error to browser's console
//             console.log(errorThrown.toString());
//         });
//         showInfo(marker);
//     });
// }
