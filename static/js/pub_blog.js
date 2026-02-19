window.onload = function (){   //在网页加载完之后再去执行这个js文件
    
    function getCsrfTokenFromDOM() {
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfInput ? csrfInput.value : '';
    }

    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: '请输入...',
        MENU_CONF: {
            uploadImage: {
                server: '/upload/image/',
                fieldName: "file",
                withCredentials: true,
                headers: {
                    'X-CSRFToken': getCsrfTokenFromDOM()
                },
            },
            uploadVideo:{
                server: "/upload/video/",
                fieldName: "file",
                maxFileSize: 100 * 1024 * 1024,
                headers: {
                    'X-CSRFToken': getCsrfTokenFromDOM()
                },
            },
        },
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#submit-btn").click(function(event){
        // 阻止按钮默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let category = $('#category-select').val();
        let content = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax('/blog/pub',{
            method: "POST",
            data: { title, category, content, csrfmiddlewaretoken},
            success: function(result){
                if(result['code'] == 200){
                    let blog_id = result['data']["blog_id"]
                    // 跳转到博客详情页面
                    window.location = '/blog/detail/' + blog_id
                }
                else{
                    alert(result['message']);
                }
            }
        })
    });
}