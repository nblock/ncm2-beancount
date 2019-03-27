if get(s:, 'loaded', 0)
    finish
endif
let s:loaded = 1

let g:ncm2_beancount#proc = yarp#py3({
    \ 'module': 'ncm2_beancount',
    \ 'on_load': { -> ncm2#set_ready(g:ncm2_beancount#source)}})

let g:ncm2_beancount#source = extend(
            \ get(g:, 'ncm2_beancount#source', {}), {
            \ 'name': 'beancount',
            \ 'enable': 1,
            \ 'ready': 0,
            \ 'priority': 8,
            \ 'mark': 'bean',
            \ 'scope': ['beancount'],
            \ 'on_complete': 'ncm2_beancount#on_complete',
            \ 'on_warmup': 'ncm2_beancount#on_warmup',
            \ }, 'keep')

func! ncm2_beancount#init()
    call ncm2#register_source(g:ncm2_beancount#source)
endfunc

func! ncm2_beancount#on_warmup(ctx)
    call g:ncm2_beancount#proc.try_notify('on_warmup', a:ctx)
endfunc

func! ncm2_beancount#on_complete(ctx)
    call g:ncm2_beancount#proc.try_notify('on_complete', a:ctx)
endfunc
