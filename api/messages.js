import { createClient } from '@supabase/supabase-js';

// Read Supabase URL and anon key from environment variables
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

// Create Supabase client instance
const supabase = createClient(supabaseUrl, supabaseAnonKey);

export default async function handler(req, res) {
  if (req.method === 'GET') {
    // Fetch all messages from 'messages' table
    const { data, error } = await supabase.from('messages').select('*');
    if (error) return res.status(500).json({ error: error.message });
    return res.status(200).json(data);
  }

  if (req.method === 'POST') {
    // Add a new message to 'messages' table
    const { content } = req.body;
    if (!content) return res.status(400).json({ error: 'Content is required' });

    const { data, error } = await supabase.from('messages').insert([{ content }]);
    if (error) return res.status(500).json({ error: error.message });

    return res.status(201).json(data);
  }

  // Other methods not allowed
  res.status(405).json({ error: 'Method not allowed' });
}
