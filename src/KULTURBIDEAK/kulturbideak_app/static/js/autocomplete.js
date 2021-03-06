 // In a perfect world, this would be its own library file that got included
    // on the page and only the ``$(document).ready(...)`` below would be present.
    // But this is an example.
    var Autocomplete = function(options) {
      this.form_selector = options.form_selector
      this.url = options.url || '/autocomplete/'
      this.delay = parseInt(options.delay || 300)
      this.minimum_length = parseInt(options.minimum_length || 3)
      this.form_elem = null
      this.query_box = null
    }

    Autocomplete.prototype.setup = function() {
      var self = this

      this.form_elem = $(this.form_selector)
      this.query_box = this.form_elem.find('input[name=search_input]')

      // Watch the input box.
      this.query_box.on('keyup', function() {
        var query = self.query_box.val()

        if(query.length < self.minimum_length) {
          return false
        }

        self.fetch(query)
      })

	 //MADDALEN : HAU KOMENTATU DUT KLIKATZEAN AUKERATUTAKO ITEMERA JOATEKO, bILAKETA KUTXAN IDATZI BEHARREAN
      // On selecting a result, populate the search field.
      /*this.form_elem.on('click', '.ac-result', function(ev) {
        self.query_box.val($(this).text())
        $('.ac-results').remove()
        return false
      })*/
    }

    Autocomplete.prototype.fetch = function(query) {
      var self = this

      $.ajax({
        url: this.url
      , data: {
          'q': query
        }
      , success: function(data) {
          self.show_results(data)
          
        }
      })
    }

    Autocomplete.prototype.show_results = function(data) {
      // Remove any existing results.
      $('.ac-results').remove()
    
      var results = data.results || []
      var results_id = data.results_id || [] //mad
      var results_img = data.results_img || [] //mad
      var results_src = data.results_src || [] //mad
      
      
      var pathname = window.location.pathname; // Returns path only
	 
      //alert(pathname);

      if(pathname == "") // "/";
      {
      	//pathname==/cross_search ...
      	var results_wrapper = $('<div class="ac-results"></div>')
      	//var base_elem = $('<div class="result-wrapper"><a href="#" class="ac-result"></a></div>')

      	if(results.length > 0) {
        	for(var res_offset in results) {
         
         		 var base_elem = $('<div class="result-wrapper"><a href="/erakutsi_item?id='+results_id[res_offset]+'" class="ac-result"></a></div>')
        		 var elem = base_elem.clone()
         		 // Don't use .html(...) here, as you open yourself to XSS.
          		 // Really, you should use some form of templating.
         		 elem.find('.ac-result').text(results[res_offset])
         		 results_wrapper.append(elem)
        
        	}
      	}
     	else {
       		var elem = base_elem.clone()
        	elem.text("No results found.")
       		results_wrapper.append(elem)
     	}
      

      	this.query_box.after(results_wrapper)
     }
     else
    {
    	
    	//HASIERAKO PANTAILAN AUTOCOMPLETE EMAITZAK ERAKUTSI
    	if(results.length > 0) 
    	{
    		
    		
    		
    		for(var res_offset in results) 
    		{
    			var a_href="/erakutsi_item?id="+results_id[res_offset];
    			
    			var img_src=results_img[res_offset];
    			if(!img_src)
    			{
    				img_src=" /uploads/NoIrudiItem.png ";
    				
    			}
    			
    			var h2_text=results_src[res_offset];
    			
    			var p_text=results[res_offset];
    		
    			//Elementuen id-ak sortu
    			var div_id="auto"+res_offset;
    			var img_id="img"+res_offset;
    			var h2_id="h2"+res_offset;
    			var p_id="p"+res_offset;
    			var a_id="a"+res_offset;
    			
    			var div_emaitza= document.getElementById(div_id);
    			
    			var elemA=document.getElementById(a_id);
    			elemA.setAttribute('href', a_href);
    			
    			var elemImg=document.getElementById(img_id);
				elemImg.setAttribute('src', img_src);
				
				var elemH2=document.getElementById(h2_id);
				elemH2.textContent = h2_text;
				
				var elemP=document.getElementById(p_id);
				elemP.textContent = p_text;
				
				//div_emaitza.appendChild(elemImg);
				
    		}
	  		 var div_service = document.getElementById("SERVICE");
	   		 div_service.setAttribute("style", "display:block;");
	    
	    	
	
		
    	}
    	else
    	{
    		
    		var kk="else";
    	}
    	
    }
    
    }

    $(document).ready(function() {
      window.autocomplete = new Autocomplete({
        form_selector: '.autocomplete-me'
      })
      window.autocomplete.setup()
    })
