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
		// テンプレートファイルが読み込めたら
		.done(function(data) {
			$template = data;
		})
		// テンプレートファイルが読み込めなかったら
		.fail(function(data, status, errorThrown) {
			$("<div class='errmes'>").text("[Error] テンプレートファイルが読み込めませんでした ("+errorThrown+")").appendTo(setting.selector);
		})
		

		// その次にマイリストをproxy.cgi経由で取得
		$.ajax({
			url: setting.proxy+'?'+setting.mylist,
			type: 'get',
			dataType: 'json',
		})
		.done(function(data) {
			// テンプレートに従って表示
			$(setting.selector).text('');
			$.tmpl($template, data).appendTo(setting.selector);
		})
		.fail(function(data, status, errorThrown) {
			$("<div class='errmes'>").text("[Error] マイリストが読み込めませんでした ("+errorThrown+")").appendTo(setting.selector);
		});
		
	}

})(jQuery);
