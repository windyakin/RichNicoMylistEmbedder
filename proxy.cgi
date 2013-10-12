#!/usr/bin/perl

# ただの中継プロキシです

use strict;
use warnings;
use utf8;

use lib ('./lib/perl');

#use CGI::Carp qw(fatalsToBrowser);
use Data::Dumper;

use Encode;
use LWP::UserAgent;
use XML::Simple;
use JSON;
use HTML::TreeBuilder;

# メイン関数の戻り値を終了コードとする
exit(main());

sub main {

	# LWP
	my $proxy = LWP::UserAgent->new();
	$proxy->timeout(5);
	$proxy->agent("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0");

	# 取ってくる
	my $res = $proxy->get("http://www.nicovideo.jp/mylist/".($ARGV[0]||'36922986')."?rss=2.0&lang=ja-jp");

	# エラーであれば終わる
	print "Status: ".$res->status_line()."\n";
	print "Content-type: text/plain; charset=UTF-8\n\n";
	if ( $res->is_success ) { 

		# XML解析
		my $xml = XML::Simple->new(ForceArray => ['item']);
		# パース
		my $obj = $xml->XMLin($res->content())->{'channel'};

		# タイトルの不要な部分を削る
		$obj->{'title'} =~ s/^マイリスト (.*)‐ニコニコ動画$/$1/gi;

		foreach my $this (@{$obj->{'item'}}) {
			# HTML解析
			my $tree = HTML::TreeBuilder->new();
			# パース
			$tree->parse($this->{'description'});
			my %vid_info = (
				'text'		=> $tree->look_down('class', 'nico-memo')->as_text,
				'thumb'		=> $tree->look_down('class', 'nico-thumbnail')->find('img')->attr('src'),
				'date'		=> $tree->look_down('class', 'nico-info-date')->as_text(),
				'length'	=> $tree->look_down('class', 'nico-info-length')->as_text(),
			);
			# 書き換え
			$this->{'description'} = \%vid_info;
			# メモリ食うので気をつけよう
			$tree->delete;
		}

		# 表示
		print encode_utf8(JSON->new->encode($obj));

	}
	else {
		print '{"status", "'.$res->status_line().'"}';
	}

	return $res->code();

}