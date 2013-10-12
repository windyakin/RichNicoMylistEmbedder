#!/usr/bin/perl

# ただの中継プロキシです

use strict;
use warnings;
use utf8;

use lib ('./lib/perl');

use CGI::Carp qw(fatalsToBrowser);
use Data::Dumper;

use Encode;
use LWP::UserAgent;
use XML::Simple;
use JSON;

print "oppau";
# メイン関数の戻り値を終了コードとする
print "Content-type: text/plain; charset=UTF-8\n\n";
exit(main());

sub main {

	my $proxy = LWP::UserAgent->new();
	$proxy->timeout(5);
	$proxy->agent("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0");

	my $res = $proxy->get("http://www.nicovideo.jp/mylist/".($ARGV[0]||'36922986')."?rss=2.0&lang=ja-jp");

	# エラーであれば終わる
	if ( !$res->is_success ) { return $res->status_line(); }

	my $xml = new XML::Simple(ForceArray => ['item']);
	my $obj = $xml->XMLin(decode('utf-8', $res->content()))->{'channel'};

	foreach my $this (@{$obj->{'item'}}) {
		print Dumper $this;
	}

	# 表示
	#print "Content-type: text/plain; charset=UTF-8\n\n";
	#print JSON->new->encode($obj);

	return 0;
}