import React, {useEffect, useState} from 'react'
import {createRef} from 'react'
import utils from '../utils'

export default function AuthenticatedLink({
                                              url,
                                              filename,
                                              children,
                                              className,
                                              validateFunc = () => true,
                                              refreshArg = undefined,
                                              onError401 = () => undefined}) {
    const link = createRef()
    const [alreadyFetched, setAlreadyFetched] = useState(false)

    useEffect(() => {
        setAlreadyFetched(false)
    }, [url, refreshArg])

    async function download() {
        if (!validateFunc())
            return
        if (!alreadyFetched) {
            const resp = await utils.get(url)
            if (resp.status === 401){
                onError401()
                return
            }
            const blob = await resp.blob()
            const href = window.URL.createObjectURL(blob)
            if (link.current)
                link.current.href = href
        }
        link.current?.click()
        setAlreadyFetched(true)
    }

    return (
        <>
            <a ref={link}
               download={filename}/>
            <a role='button'
               onClick={download}
               className={className}>
                {children}
            </a>
        </>
    )
}
