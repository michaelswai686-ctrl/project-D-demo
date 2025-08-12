import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.SUPABASE_URL
const supabaseKey = process.env.SUPABASE_ANON_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const { data, error } = await supabase
      .from('messages')
      .select('*')
      .order('created_at', { ascending: true })
    if (error) return res.status(500).json({ error: error.message })
    return res.status(200).json(data)
  }

  if (req.method === 'POST') {
    const { content } = req.body
    if (!content) return res.status(400).json({ error: 'Content is required' })

    const { data, error } = await supabase
      .from('messages')
      .insert([{ content }])
      .select()
    if (error) return res.status(500).json({ error: error.message })

    return res.status(201).json(data[0])
  }

  res.status(405).json({ error: 'Method not allowed' })
}
