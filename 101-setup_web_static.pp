#!/usr/bin/env bash
class web_server {
  package { 'nginx':
    ensure => installed,
  }

  file { '/data/web_static/releases/test/':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0755',
  }

  file { '/data/web_static/shared/':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0755',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure  => present,
    content => 'Holberton School',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
  }

  file { '/data/web_static/current':
    ensure  => 'link',
    target  => '/data/web_static/releases/test/',
    owner   => 'ubuntu',
    group   => 'ubuntu',
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \$HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://frontendnerd.tech/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}
",
  }

  service { 'nginx':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
  }
}

include web_server
EOF

puppet apply /etc/puppetlabs/code/environments/production/manifests/webserver.pp
