import React, {useEffect, useState} from 'react'
import {createRef} from 'react'
import utils from '../utils'

export default function AuthenticatedLink({url, filename, children, className, validateFunc = () => true, refreshArg = undefined}) {
    const link = createRef()
    const [alreadyFetched, setAlreadyFetched] = useState(false)

    useEffect(() => {
        setAlreadyFetched(false)
    }, [url, refreshArg])

    async function download() {
        if (!validateFunc())
            return
        if (!alreadyFetched) {
            const result = await utils.get(url)
            const blob = await result.blob()
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
