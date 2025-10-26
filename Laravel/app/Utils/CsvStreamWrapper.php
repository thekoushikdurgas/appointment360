<?php

namespace App\Utils;

class CsvStreamWrapper
{
    private static $stream;

    public static function setStream($stream)
    {
        self::$stream = $stream;
    }

    public $context;

    public function stream_open($path, $mode, $options, &$opened_path)
    {
        return true;
    }

    public function stream_read($count)
    {
        return fread(self::$stream, $count);
    }

    public function stream_eof()
    {
        return feof(self::$stream);
    }

    public function stream_stat()
    {
        return [];
    }
}
