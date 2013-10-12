(function(){

	$(function(){

		$.fn.NicoMylistEmbedder = function( options ){
			// 設定の読み込み
			var defaults = {
				'mylist': 36922986,
				'class': ".nico_mylist"
			}
			var setting = $.extend(defaults,options);
			console.log(setting.mylist);

			// ajaxで取得するよ
			$.ajax({
				url: '../proxy.cgi?'+setting.mylist,
				type: 'get',
				dataType: 'json',
			})
			.done(function(data) {
				console.dir(data);
				$(setting.class).html('<a href="'+data.link+'">'+data.title+'</a>');
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
			
		}

	});

})();
