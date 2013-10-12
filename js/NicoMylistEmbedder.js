(function($){

	$.fn.NicoMylistEmbedder = function( options ){
		// 設定の読み込み
		var defaults = {
			'mylist': 36922986,
			'selector': ".nico_mylist",
			'template': "./js/template.html",
			'proxy': "./proxy.cgi",
		};
		
		var setting = $.extend(defaults,options);
		console.log(setting.mylist);

		var $template = null;

		// まずテンプレートファイルを取得
		$.ajax({
			url: setting.template,
			type: 'get',
			dataType: 'html',
		})
		.done(function(data) {
			$template = data;
		})
		.fail(function() {
			console.log("テンプレートファイルが読み込めませんでした");
		})
		.always(function() {
		});
		

		// その次にマイリストをproxy.cgi経由で取得
		$.ajax({
			url: setting.proxy+'?'+setting.mylist,
			type: 'get',
			dataType: 'json',
		})
		.done(function(data) {
			console.dir(data);
			// テンプレートに従って表示
			$.tmpl($template, data).appendTo(setting.selector);
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
		});
		
	}

})(jQuery);
