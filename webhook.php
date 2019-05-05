<?php
/**
 * fanhaobai.com ��վ webhooks ��
 * @author fanhaobai & i@fanhaobai.com
 * @date 2019/2/1
 */
class Webhook
{
    public $config;
    public $start;
    public $end;
    public $post;
    /**
     * ���췽��
     */
    public function __construct($config)
    {
        //ע���쳣����
        set_exception_handler([$this, 'exceptionHandler']);
        if (!isset($config['token_field'])) {
            throw new Exception('token field not be set');
        }
        if (!isset($config['access_token'])) {
            throw new Exception('access token not be set');
        }
        if (!file_exists($config['bash_path'])) {
            throw new Exception('access token not be set');
        }
        //Ĭ������
        $config['log_path'] = isset($config['log_path']) ? : __DIR__ . '/';
        $config['log_name'] = isset($config['log_name']) ? : 'update_git.log';
        $config['branch'] = isset($config['branch']) ? : 'master';
        $this->config = $config;
        $this->start = $this->microtime();
        $this->accessLog('-');
        $this->accessLog('start');
        $this->post = json_decode($_POST['payload'] ?: '[]', true);
    }
    /**
     * ���
     */
    public function run()
    {
        //У��token
        if ($this->checkToken()) {
            echo 'ok';
        } else {
            echo 'error';
        }
        //��ǰ������Ӧ
        fastcgi_finish_request();
        if ($this->checkBranch()) {
            $this->exec();
        }
    }
    /**
     * У��access_token
     */
    public function checkToken()
    {
        $field = 'HTTP_' . str_replace('-', '_', strtoupper($this->config['token_field']));
        //��ȡtoken
        if (!isset($_SERVER[$field])) {
            throw new Exception('access token not be in header');
        }
        $payload = file_get_contents('php://input');
        list($algo, $hash) = explode('=', $_SERVER[$field], 2);
        //����ǩ��
        $payloadHash = hash_hmac($algo, $payload, $this->config['access_token']);
        //token����
        if (strcmp($hash, $payloadHash) != 0) {
            throw new Exception('access token check failed');
        }
        $this->accessLog('access token is ok');
        return true;
    }
    /**
     * У���֧
     */
    public function checkBranch()
    {
        $current = substr(strrchr($this->post['ref'], "/"), 1);
        $this->accessLog("branch is $current");
        return $current == $this->config['branch'];
    }
    /**
     * ִ��shell
     */
    public function exec()
    {
        $path = $this->config['bash_path'];
        $result = shell_exec("sh $path 2>&1");
        $this->accessLog($result);
        return $result;
    }
    /**
     * �쳣����
     * @param $exception
     */
    public function exceptionHandler($exception)
    {
        $msg = $exception->getMessage();
        $this->errorLog($msg);
        exit($msg);
    }
    /**
     * ������־,��¼���в���
     */
    private function accessLog($accessMessage)
    {
        //�������
        $accessMessage = date(DATE_RFC822) . " -access- " . $accessMessage . "\r\n";
        //����д�뺯��
        $this->addToFile($this->config['log_path'] . $this->config['log_name'], $accessMessage);
    }
    /**
     * ������־
     */
    private function errorLog($errorMessage)
    {
        //��ӱ�Ҫ����
        $errorMessage = date(DATE_RFC822) . " -error- " . $errorMessage . "\r\n";
        //����д�뺯��
        $this->addToFile($this->config['log_path'] . $this->config['log_name'], $errorMessage);
    }
    /**
     * д���ļ�����
     */
    private function addToFile($filePath, $logMessage, $replace = false)
    {
        //�жϴ洢�ļ�����
        $this->fileConf($filePath);
        //�����ļ�����
        if ($replace) {
            $result = file_put_contents($filePath, $logMessage);
        } else {
            $result = file_put_contents($filePath, $logMessage, FILE_APPEND);
        }
        return $result;
    }
    /**
     * ��������
     */
    public function __destruct()
    {
        $this->end = $this->microtime();
        $time = $this->end - $this->start;
        $this->accessLog('used time:' . $time);
        $memory = $this->memory();
        $this->accessLog('used memory:' . $memory);
        $this->accessLog('end');
    }
    /**
     * ʱ�����
     */
    private function microtime()
    {
        list($usec, $sec) = explode(" ", microtime(), 2);
        return ((float)$usec + (float)$sec);
    }
    /**
     * �ڴ����
     */
    private function memory()
    {
        $memory = (!function_exists('memory_get_usage')) ? '0' : round(memory_get_usage() / 1024 / 1024, 5) . 'MB';
        return $memory;
    }
    /**
     * �洢�ļ�����
     */
    private function fileConf($filePath)
    {
        $path = pathinfo($filePath);
        //·����Ŀ¼�Ƿ����
        if (!file_exists($path['dirname'])) {
            mkdir($path['dirname'], 0777, true);
        }
        //�ļ��Ƿ����
        if (!file_exists($filePath)) {
            touch($filePath);
        }
    }
}